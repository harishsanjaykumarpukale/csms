from app import app,db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route("/")
@app.route("/home")
@login_required
def home():
    if current_user.type == "student":
        return redirect(url_for('s_home'))
    
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
        if (user is None) or (user.check_password(str(form.password.data))) :
            if user is None:
                flash("Invalid user","danger")
            else:
                flash("Invalid password ","danger")
                # print(form.password.data)
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

@app.route("/register",methods = ['GET','POST'])
def register():
    # form  = 
    return render_template('register.html', )

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
    return "Chome"

@app.route("/p_home")
@login_required
def p_home():
    return "Phome"

@app.route("/s_register", methods = ['GET','POST'])
def s_register():
    return "Sregister"

@app.route("/c_register", methods = ['GET','POST'])
def c_register():
    return "Cregister"

@app.route("/p_register", methods = ['GET','POST'])
def p_register():
    return "Pregister"
