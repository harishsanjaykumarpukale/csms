from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User,Student
from flask_wtf.file import FileField, FileAllowed, FileRequired
import re


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators = [DataRequired(),EqualTo('password', message='Passwords must match')])
    f_name = StringField('First Name', validators = [DataRequired()])
    l_name = StringField('Last Name', validators = [DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email_id=email.data).first()
        if user is not None:
            raise ValidationError("This email-id is already registered !!")
    
    def validate_password(self, password):
        if len(password.data)<6 or len(password.data)>14:
            raise ValidationError("Password length should be between 6 to 14")

        if re.search("(?=.*?[A-Z])", password.data) is None:
            raise ValidationError("Password must have atleast one Uppercase letter")
        
        if re.search("(?=.*?[a-z])", password.data) is None:
            raise ValidationError("Password must have atleast one Lowercase letter")
        
        if re.search("(?=.*?[0-9])", password.data) is None:
            raise ValidationError("Password must have atleast one digit ")
        

class StudentRegForm(RegistrationForm):
    
    usn = StringField('USN', validators = [DataRequired()])
    c_email = StringField('Counsellor\'s email-id', validators = [Email()])
    departments = ['CSE','ISE','ECE']
    dept_id = SelectField('Department',choices=departments,validators=[DataRequired()])

    def validate_usn(self, usn):
        student = Student.query.filter_by(usn = usn.data).first()
        if student is not None:
            raise ValidationError("This USN is already registered!! Contact admin for help ")

class ConsellorRegForm(RegistrationForm):

    departments = ['CSE','ISE','ECE']
    dept_id = SelectField('Department',choices=departments,validators=[DataRequired()])

class ParentRegForm(RegistrationForm):
    s_email = StringField('Student\'s email-id', validators = [Email(), DataRequired()])
    c_email = StringField('Counsellor\'s email-id', validators = [Email(), DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    


# class UpdateAccountForm(FlaskForm):
#     username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',validators=[DataRequired(), Email()])
#     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Update')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('That email is taken. Please choose a different one.')


class OCRInputForm(FlaskForm):
    file = FileField('Choose the PDF file of Registration', validators = [FileRequired(), FileAllowed(['pdf'],"PDF only")])
    submit = SubmitField('Upload')