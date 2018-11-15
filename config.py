import os


class Config(object):
    SECRET_KEY = '7q%3=;8J+X5:f.+pU9e!;6x:E*n_9^Ky0~.R'


class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://administrador:ha260182ha@192.168.15.45/vehiculos'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/vehiculos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath("static/uploads/")