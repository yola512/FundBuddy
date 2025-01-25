from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route("/")
def homepage():
    return render_template("index.html")

# ensure that dashboard is displayed for logged-in user
@views.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


