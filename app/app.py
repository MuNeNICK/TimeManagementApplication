from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app) 
from models import user
from models import learning_record

login_manager = LoginManager()
login_manager.init_app(app)


import views

if __name__ == '__main__':
    app.run(host='localhost')

