from datetime import datetime, timedelta
from .models import db, Income, Expenses
from sqlalchemy import func

def get_income_by_period(period):
    today = datetime.today()
    if period == "this-year":
        # get income for this year
        start_date = datetime(today.year, 1, 1)
        return db.session.query(func.sum(Income.amount)).filter(Income.date >= start_date).scalar() or 0
    elif period == "this-month":
        # get income for this month
        start_date = datetime(today.year, today.month, 1)
        return db.session.query(func.sum(Income.amount)).filter(Income.date >= start_date).scalar() or 0
    elif period == "this-day":
        # get income for today
        start_date = datetime(today.year, today.month, today.day)
        return db.session.query(func.sum(Income.amount)).filter(Income.date >= start_date).scalar() or 0
    elif period == "last-year":
        # get income for last year
        start_date = datetime(today.year - 1, 1, 1)
        end_date = datetime(today.year - 1, 12, 31)
        return db.session.query(func.sum(Income.amount)).filter(Income.date >= start_date, Income.date <= end_date).scalar() or 0
    elif period == "last-month":
        # get income for last month
        first_day_last_month = today.replace(day=1) - timedelta(days=1)
        start_date = first_day_last_month.replace(day=1)
        end_date = first_day_last_month.replace(day=1) + timedelta(days=32)
        return db.session.query(func.sum(Income.amount)).filter(Income.date >= start_date, Income.date < end_date).scalar() or 0
    else:
        return 0

def get_expenses_by_period(period):
    today = datetime.today()
    if period == "this-year":
        # get expenses for this year
        start_date = datetime(today.year, 1, 1)
        return db.session.query(func.sum(Expenses.amount)).filter(Expenses.date >= start_date).scalar() or 0
    elif period == "this-month":
        # get expenses for this month
        start_date = datetime(today.year, today.month, 1)
        return db.session.query(func.sum(Expenses.amount)).filter(Expenses.date >= start_date).scalar() or 0
    elif period == "this-day":
        # get expenses for today
        start_date = datetime(today.year, today.month, today.day)
        return db.session.query(func.sum(Expenses.amount)).filter(Expenses.date >= start_date).scalar() or 0
    elif period == "last-year":
        # get expenses for last year
        start_date = datetime(today.year - 1, 1, 1)
        end_date = datetime(today.year - 1, 12, 31)
        return db.session.query(func.sum(Expenses.amount)).filter(Expenses.date >= start_date, Expenses.date <= end_date).scalar() or 0
    elif period == "last-month":
        # get expenses for last month
        first_day_last_month = today.replace(day=1) - timedelta(days=1)
        start_date = first_day_last_month.replace(day=1)
        end_date = first_day_last_month.replace(day=1) + timedelta(days=32)
        return db.session.query(func.sum(Expenses.amount)).filter(Expenses.date >= start_date, Expenses.date < end_date).scalar() or 0
    else:
        return 0