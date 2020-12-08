from app import app,db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, StudentRegForm, ConsellorRegForm, ParentRegForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Student, Counsellor, Parent
from werkzeug.urls import url_parse

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
    return render_template('index.html',title = "Home")

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
            if user is None:
                flash("Invalid user","danger")
            else:
                flash("Invalid password ","danger")
                print(form.password.data)
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
    return render_template('s_home.html')

@app.route("/c_home")
@login_required
def c_home():
    return render_template('c_home.html')

@app.route("/p_home")
@login_required
def p_home():
    return render_template('p_home.html')

@app.route("/s_register", methods = ['GET','POST'])
def s_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = StudentRegForm()

    if form.validate_on_submit():
        user = User(email_id = form.email.data, type = "student")
        user.set_password(form.password.data)
        db.session.add(user)
        student = Student(s_email_id = form.email.data, f_name = form.f_name.data, l_name = form.l_name.data, usn = form.usn.data, c_email_id = form.c_email.data)
        db.session.add(student)

        db.session.commit()

        flash("You have registerd succesfully!! ","success")

        return redirect(url_for('login'))
    
    return render_template('s_reg.html', form = form)

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

    return render_template('c_reg.html', form = form)

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
    return render_template('p_reg.html', form = form)
