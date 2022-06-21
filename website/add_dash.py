
from unicodedata import category
from flask import Flask, Blueprint, render_template,  flash
import urllib.request

from flask_login import  login_required , current_user
from .models import Note
from .import db
import json
import os
from .form import UserDataForm
from .models import IncomeExpenses


add_dash = Blueprint('add_dash', __name__)


@add_dash.route('/index')
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template("index.html", user=current_user, entries=entries)


@add_dash.route('/add_dash', methods =['GET', 'POST'])
def add_expense():
    form = UserDataForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type = form.type.data,
                              amount = form.amount.data, 
                              category = form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash("Successful")
        

                              
    return render_template("add.html", title = 'layout', form = form, user=current_user)

@add_dash.route('/delete/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deletion was successful", 'success')
    return render_template("index.html", user=current_user)



@add_dash.route('/chart')
def chart():
    income_vs_expenses = db.session.query(db.func.sum(IncomeExpenses.amount),
    IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), 
    IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()



    income_expenses = []
    for total_amount, _ in income_vs_expenses:
        income_expenses.append(total_amount)


    over_time_expenditure = []
    dates_labels = []
    for amount, date in dates:
        
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime("%m-%d-%Y"))
        
    return render_template("chart.html", user=current_user, 
                           income_vs_expenses = json.dumps(income_expenses),
                           over_time_expenditure=json.dumps(over_time_expenditure),
                           dates_labels = json.dumps(dates_labels))
    
                           
 