from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User,Student


# class RegistrationForm(FlaskForm):
    # username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField('Email',validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    # submit = SubmitField('Sign Up')
# 
    # def validate_username(self, username):
        # user = User.query.filter_by(username=username.data).first()
        # if user:
            # raise ValidationError('That username is taken. Please choose a different one.')
# 
    # def validate_email(self, email):
        # user = User.query.filter_by(email=email.data).first()
        # if user:
            # raise ValidationError('That email is taken. Please choose a different one.')

class StudentRegForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators = [DataRequired(),EqualTo('password')])
    usn = StringField('USN', validators = [DataRequired()])
    f_name = StringField('First Name', validators = [DataRequired()])
    l_name = StringField('Last Name', validators = [DataRequired()])
    c_email = StringField('Counsellor\'s email-id', validators = [Email()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email_id=email.data).first()
        if user is not None:
            raise ValidationError("This email-id is already registered !!")
    
    def validate_usn(self, usn):
        student = Student.query.filter_by(usn = usn.data).first()
        if student is not None:
            raise ValidationError("This USN is already registered!! Contact admin for help ")


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
