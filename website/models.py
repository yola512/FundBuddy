from . import db #import from current package (so from website, we can import bc of __init__.py)
from flask_login import UserMixin 
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, Currency, CurrencyType, force_auto_coercion
import re

force_auto_coercion()

class User(db.Model, UserMixin): 
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    email = db.Column(EmailType, nullable = False, unique = True)
    password = db.Column(db.String(150), nullable = False)
    incomes = db.relationship('Income', backref = 'user')
    expenses = db.relationship('Expenses', backref = 'user')
    savings = db.relationship('Savings', backref = 'user')

class Income(db.Model):
    __tablename__ = 'Incomes'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable = False)
    amount = db.Column(db.Numeric(10,2), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable = False)
    currency = db.Column(CurrencyType, nullable = False)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    description = db.Column(db.String(300))

    # relationship with category
    category = db.relationship('Category', backref='incomes')

class Category(db.Model):
    __tablename__ = 'Categories'
    id = db.Column(db.Integer, primary_key = True)
    cat_name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(300)) 

class Expenses(db.Model):
    __tablename__ = 'Expenses'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable = False)
    amount = db.Column(db.Numeric(10,2), nullable = False)
    currency = db.Column(CurrencyType, nullable = False)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable = False)

    # relationship with category
    category = db.relationship('Category', backref='expenses')

class Savings(db.Model):
    __tablename__ = 'Savings'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable = False)
    goal = db.Column(db.String(300)) # optional goal description
    total_savings = db.Column(db.Numeric(10,2), nullable = False) # numeric(10,.) bc it's a personal expense tracker and i dont think the transactions will be larger than 99 million  
    currency = db.Column(CurrencyType, nullable = False)