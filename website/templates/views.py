from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user
from website import db
from website.models import Income, Category, Expenses

views = Blueprint('views', __name__)

@views.route("/")
def homepage():
    return render_template("index.html")

# ensure that dashboard is displayed for logged-in user
@views.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# Insights
@views.route("/insights")
@login_required
def insights():
    return render_template("insights.html", user=current_user)

# Expenses
@views.route("/expenses")
@login_required
def expenses():
    return render_template("expenses.html", user=current_user)

# Income
@views.route("/income")
@login_required
def income():
    user_incomes = Income.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.all() # get categories from database
    return render_template('income.html', incomes=user_incomes, categories=categories)

# Income - adding to database
@views.route("/income/add_incomes",  methods=['POST'])
@login_required
def add_incomes():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category_id = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')

        # if 'date' is a string -> convert to DateTime object
        from datetime import datetime
        date = datetime.strptime(date, "%Y-%m-%d")

        new_income = Income(
            amount=amount,
            currency="USD", # default USD, -> later add other currencies
            date=date,
            category_id=category_id,
            description=description,
            user_id=current_user.id # assign to logged-in user
        )

        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('income'))
    
    
# Categories
@views.route("/categories")
@login_required
def categories():
    return render_template("categories.html", user=current_user)

# Savings
@views.route("/savings")
@login_required
def savings():
    return render_template("savings.html", user=current_user)

