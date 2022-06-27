import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///tma_flask.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(24)