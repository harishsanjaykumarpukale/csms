from app import app,db,mongo
from flask import render_template, flash, redirect, url_for, request
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse
from OCR.ocr_student_pdf import get_student_details
from datetime import date

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
    return render_template('student/s_home.html')

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
    code = request.args.get('course_code', 0, type=str)
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
    
    USN = Student.query.filter_by(s_email_id = current_user.email_id).first().usn
    data = mongo.db.attd.find_one({ "usn" : USN })

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

    return render_template('student/s_attendance.html', attd = data, courses = course_list, forms = form_list)