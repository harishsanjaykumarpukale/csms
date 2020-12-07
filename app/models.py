from app import db,login
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
    email_id = db.Column(db.String(120), primary_key = True)
    password_hash = db.Column(db.String(128), nullable = False)
    type = db.Column(db.String(20), nullable = False) # 3 types - Student, Counsellor and Teacher

    def __repr__(self):
        return '<User {}>'.format(self.email_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = "Student"
    s_email_id = db.Column(db.String(120), primary_key = True)
    usn = db.Column(db.String(10), unique = True, nullable = False)
    f_name = db.Column(db.String(250), nullable = False)
    l_name = db.Column(db.String(250), nullable = False)
    c_email_id = db.Column(db.String(120),db.ForeignKey('Counsellor.c_email_id'),default = 'counsellor@gmail.com')

class Counsellor(db.Model):
    __tablename__ = "Counsellor"
    c_email_id = db.Column(db.String(120), primary_key = True)
    f_name = db.Column(db.String(250), nullable = False)
    l_name = db.Column(db.String(250), nullable = False)
    dept_id = db.Column(db.String(5),db.ForeignKey('Department.dept_id'))

    counsellees = db.relationship('Student', backref = db.backref('counsellor',lazy = 'joined'), lazy = 'subquery')

class Parent(db.Model):
    __tablename__ = "Parent"
    p_email_id = db.Column(db.String(120), primary_key = True)
    f_name = db.Column(db.String(250),nullable = False)
    l_name = db.Column(db.String(250),nullable = False)
    c_email_id = db.Column(db.String(120),db.ForeignKey('Counsellor.c_email_id'))
    s_email_id = db.Column(db.String(120),db.ForeignKey('Student.s_email_id'))

    child = db.relationship('Student', backref = db.backref('parent', lazy = 'joined'), lazy = 'joined')
    counsellor = db.relationship('Counsellor', backref = db.backref('parent', lazy = 'select'), lazy = 'joined')
    

class Department(db.Model):
    __tablename__ = "Department"
    dept_id = db.Column(db.String(5), primary_key = True)
    dept_name = db.Column(db.String(20),nullable = False)
    hod_email_id = db.Column(db.String(120),db.ForeignKey('Counsellor.c_email_id'))

    # hod = db.relationship('Counsellor', backref = db.backref('managing-department', lazy = 'select'), lazy = 'joined')
    professors = db.relationship('Counsellor', foreign_keys = 'Counsellor.dept_id', backref = db.backref('department', lazy = 'joined'), lazy = 'select')

ql = get_debug_queries()
print(ql)