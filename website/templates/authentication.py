from flask import Blueprint, render_template, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from website.models import User
from website import db
import re


auth_bp = Blueprint('auth', __name__)

#log in
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       email = request.form.get('email')
       password = request.form.get('password')

       # data validation
       user = User.query.filter_by(email=email).first()
       if user and check_password_hash(user.password, password):
          login_user(user)
          flash("Logged in successfully", category='success')
          return redirect(url_for('views.dashboard'))
       else:
          flash("Invalid email or password", category='error')

    return render_template('login.html')

#sign up
@auth_bp.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
      first_name = request.form.get('first_name')
      email = request.form.get('email')
      password = request.form.get('password')
      confirm_password = request.form.get('confirm_password')
    
      # data validation
      user = User.query.filter_by(email=email).first()
      # if email already exists in the database -> display proper error message
      if user:
         flash("Email already exists", category = 'error')
      elif not validate_password():
         flash("Password must have at least 8 characters, min. 1 uppercase letter, min. 1 lowercase letter and min. 1 digit", category='error')
      elif password != confirm_password:
         flash("Passwords don't match", category='error')
      else:
         # add new user to database
         new_user = User(first_name=first_name,
                         email=email,
                         password=generate_password_hash(password))
         db.session.add(new_user)
         db.session.commit()
         flash("Account created successfully! :)", category='success')
         return redirect(url_for("auth.login"))

    return render_template('signup.html')


# validate password using regex: min.: 8 characters, 1 uppercase letter, 1 lowercase letter, 1 digit
def validate_password(password):
   pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
   if re.match(pattern, password):
      return True
   return False