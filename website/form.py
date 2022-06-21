
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class UserDataForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                                choices=[('Income', 'Income'),
                                        ('Expense', 'Expense')])
    category = SelectField("Category", validators=[DataRequired()],
                                            choices =[('Rent', 'Rent'),
                                            ('Salary', 'Salary'),
                                            ('Investment', 'Investment'),
                                            ('Side_hustle', 'Side_hustle')
                                            ]
                            )
    amount = IntegerField('Amount', validators = [DataRequired()])                                   
    submit = SubmitField('Generate Report')     