import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5791628bb0b13ce0c676dfde280ba245'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir , 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = False

    MONGO_URI = os.environ.get('MONGO_DATABSE_URI') or 'mongodb://localhost:27017/test'

    MAX_CONTENT_LENGTH = 500 * 1024 
    
    # define a folder to store and later serve the images
    UPLOAD_FOLDER = '/uploads/'

