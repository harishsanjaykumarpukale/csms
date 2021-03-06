from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import get_debug_queries


@login.user_loader
def load_user(email_id):
    return User.query.get(email_id)


def get_email_id(self):
    return self.email_id


UserMixin.get_id = get_email_id


class User(db.Model, UserMixin):
    __tablename__ = "Credentials"
    email_id = db.Column(db.String(120), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    # 3 types - Student, Counsellor and Teacher
    type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.email_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    __tablename__ = "Student"
    s_email_id = db.Column(db.String(120), primary_key=True)
    usn = db.Column(db.String(10), unique=True, nullable=False)
    f_name = db.Column(db.String(250), nullable=False)
    l_name = db.Column(db.String(250), nullable=False)
    doj = db.Column(db.Date, nullable=False)
    dept_id = db.Column(db.String(5), db.ForeignKey('Department.dept_id'))
    c_email_id = db.Column(db.String(120), db.ForeignKey(
        'Counsellor.c_email_id'), default='counsellor@gmail.com')

ProfessorCourseDetails = db.Table("ProfessorCourseDetails",db.Column('c_email_id',db.String(120), db.ForeignKey('Counsellor.c_email_id'), primary_key=True),db.Column('course_code',db.String(120), db.ForeignKey('Course.course_code'), primary_key=True))


class Counsellor(db.Model):
    __tablename__ = "Counsellor"
    c_email_id = db.Column(db.String(120), primary_key=True)
    f_name = db.Column(db.String(250), nullable=False)
    l_name = db.Column(db.String(250), nullable=False)
    dept_id = db.Column(db.String(5), db.ForeignKey('Department.dept_id'))

    counsellees = db.relationship('Student', backref=db.backref(
        'counsellor', lazy='joined'), lazy='subquery')
    
    courses = db.relationship('Course', secondary = ProfessorCourseDetails, lazy = True, backref = db.backref('professor', lazy = True))


class Parent(db.Model):
    __tablename__ = "Parent"
    p_email_id = db.Column(db.String(120), primary_key=True)
    f_name = db.Column(db.String(250), nullable=False)
    l_name = db.Column(db.String(250), nullable=False)
    c_email_id = db.Column(
        db.String(120), db.ForeignKey('Counsellor.c_email_id'))
    s_email_id = db.Column(db.String(120), db.ForeignKey('Student.s_email_id'))

    child = db.relationship('Student', backref=db.backref(
        'parent', lazy='joined'), lazy='joined')
    counsellor = db.relationship('Counsellor', backref=db.backref(
        'parent', lazy='select'), lazy='joined')


class Department(db.Model):
    __tablename__ = "Department"
    dept_id = db.Column(db.String(5), primary_key=True)
    dept_name = db.Column(db.String(20), nullable=False)
    h_email_id = db.Column(db.String(120), db.ForeignKey(
        'Counsellor.c_email_id'), default = 'principal@rvce.edu.in')

    hod = db.relationship(
        'Counsellor',
        uselist = False,
        backref=db.backref(
            'managing-department',
            lazy='select',
            uselist=False),
        lazy='select',
        primaryjoin='Department.h_email_id==Counsellor.c_email_id',
        post_update=True)
    professors = db.relationship(
        'Counsellor',
        foreign_keys='Counsellor.dept_id',
        backref=db.backref(
            'department',
            lazy='select',
            uselist = False),
        lazy='select')


class Course(db.Model):
    __tablename__ = "Course"
    course_code = db.Column(db.String(10), primary_key=True)
    course_name = db.Column(db.String(20), nullable=False)
    dept_id = db.Column(db.String(5), db.ForeignKey('Department.dept_id'))
    # dept = db.relationship()
    sem_date = db.Column(db.Date, nullable = False)

class StudentCourseDetails(db.Model):
    __tablename__ = "StudentCourseDetails"
    s_email_id = db.Column(db.String(120), db.ForeignKey('Student.s_email_id'), primary_key=True)
    course_code = db.Column(db.String(10), db.ForeignKey('Course.course_code'), primary_key=True)
    date = db.Column(db.Date, primary_key = True)

# ProfessorCourseDetails = db.Table("ProfessorCourseDetails",db.Column('c_email_id',db.String(120), db.ForeignKey('Counsellor.c_email_id'), primary_key=True),db.Column('course_code',db.String(120), db.ForeignKey('Course.course_code'), primary_key=True))


PhoneNumbers = db.Table("PhoneNumbers", db.Column('email_id',db.String(120),db.ForeignKey('Credentials.email_id'), primary_key=True),db.Column('phone_number',db.Integer(), db.ForeignKey('PhoneNumber.phone_number'), primary_key=True))

class PhoneNumber(db.Model):
    __tablename__ = "PhoneNumber"
    phone_number = db.Column(db.Integer(), primary_key=True)
    user = db.relationship('User', secondary = PhoneNumbers, lazy = True, backref = db.backref('phone_numbers', lazy = True))




# ql = get_debug_queries()
# print(ql)
