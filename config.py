import os


class Config(object):
    SECRET_KEY = '7417q%3=;8J+X5:f.+pU9e!;6x:E*n_9^Ky0~.R369'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://pascual:lh260182lh@192.168.15.211/vehiculos'
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:ha260182ha@localhost/vehiculos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath("static/uploads/")
