from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
from os import path
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()

def create_app():
  # create the app
  app = Flask(__name__)
  # secret_key for security
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
  # configure the SQLite database
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  
  # initialize the app 
  db.init_app(app)
  migrate = Migrate(app, db)  # initialize Flask-Migrate

  
  from website.templates.views import views
  from website.templates.authentication import auth_bp

  app.register_blueprint(views, url_prefix = '/')
  app.register_blueprint(auth_bp, url_prefix = '/') 

  from website.models import User, Income, Category, Expenses, Savings  # to make sure that models.py runs and defines the classes before we initialize our database
  
  # creating database
  # sqlAlchemy wont overwrite an existing file, the only time the database wont be created is if it raised an error
  with app.app_context():
    db.create_all()

 # configuring app
  login_manager = LoginManager()
  login_manager.login_view = "auth.login" 
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))
  
  return app
