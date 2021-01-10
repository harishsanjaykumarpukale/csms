from app import app,db,mongo
from flask import render_template, flash, redirect, url_for, request
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse
from OCR.ocr_student_pdf import get_student_details
from datetime import date
from bson.json_util import dumps
from pdfkit import from_string
from flask.helpers import make_response, send_file
from bson.binary import Binary
from bson.objectid import ObjectId

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['pdf'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@app.route("/home")
@login_required
def home():
    if current_user.type == "student":
        return redirect(url_for('s_home'))
    if current_user.type == "counsellor":
        return redirect(url_for('c_home'))
    if current_user.type == "parent":
        return redirect(url_for('p_home'))
    return render_template('404.html',title = "404")

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_id = form.email.data).first()
        if (user is None) or (not user.check_password(form.password.data)) :
            # if user is None:
            #     flash("Invalid user","danger")
            # else:
            #     flash("Invalid password ","danger")
            #     print(form.password.data)
            flash('Invalid email-id or password','danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if  not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html',title = "Login" , form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
def account():
    return "Account"

@app.route("/s_home")
@login_required
def s_home():
    student = Student.query.filter_by(s_email_id = current_user.email_id).first()
    USN = student.usn
    grade = mongo.db.grade.find_one({ "usn" : USN})
    if grade is not None:
        return render_template('student/s_home.html', cgpa = grade['cgpa'])
    return render_template('student/s_home.html', cgpa = "" )

@app.route("/c_home")
@login_required
def c_home():
    return render_template('counsellor/c_home.html')

@app.route("/p_home")
@login_required
def p_home():
    return render_template('parent/p_home.html')

@app.route("/s_register", methods = ['GET','POST'])
def s_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = StudentRegForm()

    if form.validate_on_submit():
        user = User(email_id = form.email.data, type = "student")
        user.set_password(form.password.data)
        db.session.add(user)
        student = Student(s_email_id = form.email.data, f_name = form.f_name.data, l_name = form.l_name.data, usn = form.usn.data, dept_id = form.dept_id.data, doj = date(2000+int(form.usn.data[3:5]),7,1), c_email_id = form.c_email.data)
        db.session.add(student)

        db.session.commit()

        flash("You have registerd succesfully!! ","success")

        return redirect(url_for('login'))
    
    return render_template('student/s_reg.html', form = form)

@app.route("/c_register", methods = ['GET','POST'])
def c_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = ConsellorRegForm()
    if form.validate_on_submit():
        user = User(email_id = form.email.data, type = "counsellor")
        user.set_password(form.password.data)
        db.session.add(user)

        counsellor = Counsellor(c_email_id = form.email.data, f_name = form.f_name.data, l_name = form.l_name.data, dept_id = form.dept_id.data )
        db.session.add(counsellor)

        db.session.commit()

        flash("You have registerd succesfully!! ","success")

        return redirect(url_for('login'))

    return render_template('counsellor/c_reg.html', form = form)

@app.route("/p_register", methods = ['GET','POST'])
def p_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = ParentRegForm()
    if form.validate_on_submit():
        user = User(email_id = form.email.data, type = "parent")
        user.set_password(form.password.data)
        db.session.add(user)

        parent = Parent(p_email_id = form.email.data, f_name = form.f_name.data, l_name = form.l_name.data, c_email_id = form.c_email.data, s_email_id = form.s_email.data)
        db.session.add(parent)

        db.session.commit()
        
        flash("You have registerd succesfully!! ","success")

        return redirect(url_for('login'))
    return render_template('parent/p_reg.html', form = form)

@app.route("/reg_ocr", methods = ['GET','POST'])
def reg_ocr():
    form = OCRInputForm()
    if request.method == 'POST':

        # check if there is a file in the request
        if 'file' not in request.files:
            flash("No file selected","error")
            return redirect(url_for('reg_ocr'))
        
        file = request.files['file']
        
        # if no file is selected
        if file.filename == '':
            flash("No file selected","error")
            return redirect(url_for('reg_ocr'))
        
        if not allowed_file(file.filename):
            flash("Only PDF files allowed ","error")
            return redirect(url_for('reg_ocr'))
        
        if file and allowed_file(file.filename):
            student = get_student_details(file.read())
            print(student)
            user = User(email_id = student['s_email'], type = "student")
            userexists = User.query.filter_by(email_id=user.email_id).first()
            if userexists is not None:
                flash("Student already registered","danger")
                return redirect(url_for('reg_ocr'))
            
            user.set_password("Ab1234")
            db.session.add(user)
            student = Student(s_email_id = student['s_email'], f_name = student['f_name'], l_name = student['l_name'], usn = student['usn'], dept_id = student['usn'][5:7]+"E", doj = date(2000+int(student['usn'][3:5]),7,1),c_email_id = student['c_email'])
            db.session.add(student)

            db.session.commit()

            flash("You have registerd succesfully!! ","success")

            return render_template('student/reg_ocr.html',title = "Successful Registration - CSMS", form = form,txtrecgnised = student)

    return render_template('student/reg_ocr.html', title = "Upload PDF", form = form)


@app.route("/s_assessment")
@login_required
def s_assessment():
    # print(current_user.email_id)
    course_code_list = StudentCourseDetails.query.filter_by(s_email_id = current_user.email_id, date = date(2020, 7, 1))
    
    course_list = []

    for each in course_code_list:
        course = Course.query.filter_by(course_code = each.course_code).first()
        # print(course)
        course_list.append(course)
    
    return render_template('student/s_assessment.html', courses = course_list)

@app.route("/s_assessment_detail")
@login_required
def s_assessment_detail():
    code = request.args.get('course_code', "18CS52", type=str)
    course = Course.query.filter_by(course_code = code).first()
    USN = Student.query.filter_by(s_email_id = current_user.email_id).first().usn 
    marks = mongo.db.marks.find_one( { "usn" : USN })
    data = marks["5"][code]
    keys = ['Q1','CIE1','Q2','CIE2','Q3','CIE3']
    for each in keys:
        if each not in data.keys():
            data[each] = ""
    if data["lab"] and "LAB" not in data.keys():
        data["LAB"] = ""
    return render_template('student/s_assessment_detail.html', crs = course, marks = data)

@app.route("/s_attendance", methods = ['GET','POST'])
@login_required
def s_attendance():

    # if request.method == "POST":
    #     if form_list[0].validate_on_submit:

    
    USN = Student.query.filter_by(s_email_id = current_user.email_id).first().usn
    data = mongo.db.attd.find_one({ "usn" : USN })
    print(data)

    course_code_list = StudentCourseDetails.query.filter_by(s_email_id = current_user.email_id, date = date(2020, 7, 1))
    
    course_list = []
    form_list = []

    for each in course_code_list:
        course = Course.query.filter_by(course_code = each.course_code).first()
        # print(course)
        course_list.append(course)

        form = FileInputForm()
        form.course_code = each.course_code
        form_list.append(form)
    
    
    # if form_list[0].validate_on_submit:
    #     return redirect(url_for('s_attendance'))

    return render_template('student/s_attendance.html', attd = data, courses = course_list, forms = form_list)


@app.errorhandler(413)
def too_large(e):
    return "File is too large please upload smaller file", 413

@app.route("/s_attendance_update", methods = ["GET", "POST"])
@login_required
def s_attendance_update():
    form = FileInputForm()
    code = request.args.get('course_code', "18CS52", type=str)
    if request.method == 'POST':

        # check if there is a file in the request
        if 'file' not in request.files:
            flash("No file selected","error")
            return redirect(url_for('s_attendance_update'))
        
        file = request.files['file']
        
        # if no file is selected
        if file.filename == '':
            flash("No file selected","error")
            return redirect(url_for('s_attendance_update'))
        
        if not allowed_file(file.filename):
            flash("Only PDF files allowed ","error")
            return redirect(url_for('s_attendance_update'))
        
        if file and allowed_file(file.filename):
            student = Student.query.filter_by(s_email_id = current_user.email_id).first()
            mongo.db.reqs.update_one( { "email" : student.c_email_id }, { "$push" : { "attdreqs" : { "_id" : ObjectId() ,"code" : code, "usn" : student.usn , "approved" : False , "file" : file.read()}}})

            # mongo.db.docs.insert_one({ 'file' : file.read()})
            # s = mongo.db.docs.find_one({})
            # s = s['file']
            # response = make_response(s)
            # response.headers['Content-Type'] = "application/pdf"
            # response.headers['Content-Dispostion'] = 'inline; filename=report.pdf'

            # return response
            flash("File uploaded succesfully!! ","success")

            return redirect(url_for('s_attendance'))

    return render_template('student/s_attendance_update.html', form = form)

@app.route("/s_hss", methods = ["GET", "POST"])
@login_required
def s_hss():
    form = HSSActivityDetailForm()
    if form.validate_on_submit():
        # check if there is a file in the request
        if 'file' not in request.files:
            flash("No file selected","error")
            return redirect(url_for('s_hss'))
        
        file = request.files['file']
        
        # if no file is selected
        if file.filename == '':
            flash("No file selected","error")
            return redirect(url_for('s_hss'))
        
        if not allowed_file(file.filename):
            flash("Only PDF files allowed ","error")
            return redirect(url_for('s_hss'))
        
        if file and allowed_file(file.filename):
            student = Student.query.filter_by(s_email_id = current_user.email_id).first()
            mongo.db.reqs.update_one( { "email" : student.c_email_id }, { "$push" : { "hssreqs" : { "usn" : student.usn , "approved" : False , "activity" : { "title" : form.title.data, "descrption" : form.description.data, "file" : file.read()}}}})

            # mongo.db.docs.insert_one({ 'file' : file.read()})
            # s = mongo.db.docs.find_one({})
            # s = s['file']

            # s = mongo.db.reqs.find_one({ "email" : student.c_email_id})
            # s = s["hssreqs"][0]["activity"]["file"]
            # response = make_response(s)
            # response.headers['Content-Type'] = "application/pdf"
            # response.headers['Content-Dispostion'] = 'inline; filename=report.pdf'

            # return response
            flash("HSS Actvity details submitted succesfully!! ", "success")
            return redirect(url_for('s_home'))
    return render_template('student/s_hss.html', form = form)

@app.route("/c_report", methods = ["GET", "POST"])
@login_required
def c_report():
    form = CGPAForm()
    if request.method == 'POST':
        lmt = form.l_limit.data
        data = mongo.db.grade.find({ "cgpa" : { "$gt" : float(lmt) } })
        # data = mongo.db.grade.find({ })
        final = list(data)
        return render_template('counsellor/c_report.html', form = form, data = final, cgpa = float(lmt))
    return render_template('counsellor/c_report.html', form = form)

@app.route("/download")
def download():
    cgpa = request.args.get('cgpa', 7.0 , type = float)
    # print(cgpa)
    data = mongo.db.grade.find({ "cgpa" : { "$gt" : cgpa } })
    data = list(data)
    rendered = render_template('counsellor/report.html', data = data)
    pdf = from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Dispostion'] = 'inline; filename=report.pdf'

    return response


@app.route("/c_students")
@login_required
def c_students():
    counsellor = Counsellor.query.filter_by(c_email_id = current_user.email_id).first()
    return render_template('counsellor/c_students.html', students = counsellor.counsellees)


@app.route("/c_student_detail/<email_id>")
@login_required
def c_student_detail(email_id):
    # print(email_id)
    student = Student.query.filter_by(s_email_id = email_id).first()
    return render_template('counsellor/c_student_detail.html', student = student)

@app.route("/c_search_usn", methods = ["GET","POST"])
@login_required
def c_search_usn():
    form = SearchUSNForm()

    if form.validate_on_submit() and request.method == "POST" :
        if form.last_3_digits.data < 100:
            USN = "1RV18" + form.dept.data[0:2] + "0" + str(form.last_3_digits.data)
        else:
            USN = "1RV18" + form.dept.data[0:2] + str(form.last_3_digits.data)
        student = Student.query.filter_by(usn = USN).first()
        if student is None:
            flash("No student found","danger")
            return redirect(url_for('c_search_usn'))
        return redirect(url_for('c_student_detail', email_id = student.s_email_id))

    return render_template('counsellor/c_search_usn.html', form = form)

@app.route("/notification", methods = ["GET","POST"])
@login_required
def notification():
    q = mongo.db.reqs.find_one({ "email" : current_user.email_id})
    attd_l = q["attdreqs"]
    pending_attd_l = []
    for each in attd_l:
        if each["approved"] is False:
            pending_attd_l.append(each)
    
    if 'view' in request.args.keys():
        
        id = request.args.get('id','0',type = ObjectId)
        # print(id)
        for each in pending_attd_l:
            # print(each["_id"])
            if each["_id"] == id:
                # print("found")
                file = each["file"]
                response = make_response(file)
                response.headers['Content-Type'] = "application/pdf"
                response.headers['Content-Dispostion'] = 'inline; filename=report.pdf'
                return response
    
    return render_template('notification.html', ac = len(pending_attd_l), al = pending_attd_l)


@app.route("/update_attendance")
@login_required
def update_attendance():
    usn = request.args.get('usn','0',type = str)
    code = request.args.get('code','code', type = str)
    id = request.args.get('id','0',type = ObjectId)
    if usn == "0" or code == "code" :
        return 404
    a = mongo.db.attd.find_one({ "usn" : usn })
    total = a[code]["total"]
    p = a[code]["percentage"] + 100/total
    p = round(p,2)
    mongo.db.attd.update_one({ "usn" : usn} , { "$set" : { code+".percentage" : p}})
    mongo.db.reqs.update_one({ "email" : current_user.email_id , "attdreqs._id" : id}, { "$set" : { "attdreqs.$.approved" : True}})
    flash("Attendance Updated Successfully!!","success")
    return redirect(url_for('notification'))
