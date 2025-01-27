from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from website import db
from website.models import Income, Category, Expenses
from datetime import datetime
from website.utils import get_income_by_period, get_expenses_by_period

views = Blueprint('views', __name__)

@views.route("/")
def homepage():
    return render_template("index.html")

# ensure that dashboard is displayed for logged-in user
@views.route("/dashboard")
@login_required
def dashboard():
    income_this_year = get_income_by_period('this-year')
    expenses_this_year = get_expenses_by_period('this-year')
    income_last_year = get_income_by_period('last-year')
    expenses_last_year = get_expenses_by_period('last-year')
    # savings = calculate_savings() # not ready yet :c
    return render_template("dashboard.html", user=current_user, 
                           income_this_year=income_this_year, 
                           expenses_this_year=expenses_this_year,
                           income_last_year=income_last_year,
                           expenses_last_year=expenses_last_year)

# Insights
@views.route("/insights")
@login_required
def insights():
    return render_template("insights.html", user=current_user)

# Expenses
@views.route("/expenses")
@login_required
def expenses():
    user_expenses = Expenses.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.all() # get categories from database
    return render_template("expenses.html", expenses=user_expenses, categories=categories)

# Expenses - adding to database
@views.route("/expenses/add_expenses",  methods=['POST'])
@login_required
def add_expenses():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category_id = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')

        # if 'date' is a string -> convert to DateTime object
        date = datetime.strptime(date, "%Y-%m-%d")

        new_expenses = Expenses(
            amount=amount,
            currency="USD", # default USD, -> later add other currencies
            date=date,
            category_id=category_id,
            description=description,
            user_id=current_user.id # assign to logged-in user
        )

        db.session.add(new_expenses)
        db.session.commit()
        return redirect(url_for('views.expenses'))
    

# Income
@views.route("/income")
@login_required
def income():
    user_incomes = Income.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.all() # get categories from database

    # dynamic data for the chart
    #income_data = {
       # "This Year": sum(income.amount for income in user_incomes if income.date.year == datetime.now().year),
       # "This Month": sum(income.amount for income in user_incomes if income.date.month == datetime.now().month),
       # "Last Year": sum(income.amount for income in user_incomes if income.date.year == datetime.now().year - 1),
       # "Last Month": sum(income.amount for income in user_incomes if income.date.month == datetime.now().month - 1)
    #}

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

        if not amount or not category_id or not date:
            flash("All fields are required!", category="danger")
            return redirect(url_for('views.income'))
        

        # if 'date' is a string -> convert to DateTime object
        date = datetime.strptime(date, "%Y-%m-%d")

        new_income = Income(
            user_id=current_user.id, # assign to logged-in user
            amount=amount,
            category_id=category_id,
            currency="USD", # default USD, -> later add other currencies
            date=date,
            description=description
        )

        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('views.income'))
    

# Categories
@views.route("/categories")
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template("categories.html", categories=categories)

# Categories - adding to database
@views.route("/categories/add_category",  methods=['POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        description = request.form.get('description')

        if not category_name:
          flash("Category name is required!", category="danger")
          return redirect(url_for('views.categories'))
    
        # Check if category already exists
        existing_category = Category.query.filter_by(cat_name=category_name, user_id=current_user.id).first()
        if existing_category:
          flash("Category already exists!", category="danger")
          return redirect(url_for('views.categories'))
    
        new_category = Category(cat_name=category_name, description=description, user_id=current_user.id)
        db.session.add(new_category)
        db.session.commit()
        
        flash("Category added successfully!", category="success")
        return redirect(url_for('views.categories'))
    
    

# Savings
@views.route("/savings")
@login_required
def savings():
    return render_template("savings.html", user=current_user)

