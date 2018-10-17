import os


class Config(object):
    SECRET_KEY = '7q%3=;8J+X5:f.+pU9e!;6x:E*n_9^Ky0~.R'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://administrador:ha260182ha@127.0.0.1/vehiculos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath("static/uploads/")
