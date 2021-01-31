from flask_wtf import FlaskForm
from wtforms import  StringField,IntegerField, PasswordField, TextAreaField, DateField,  widgets
from wtforms.validators import DataRequired, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from datetime import date, timedelta
from models import *
from flask import session 
from wtforms.csrf.session import SessionCSRF

class BaseForm(FlaskForm):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'jfjasolkjiksdajfoisdfj'
        csrf_time_limit = timedelta(minutes=30)



class WorkoutForm(BaseForm):

    name = StringField('Workout Name', validators=[DataRequired()])
    date = DateField('Workout Date', default=date.today)
    time = IntegerField('Time Elapsed(min)')

class SetForm(BaseForm):
    exercise = StringField('Exercise:', validators=[DataRequired()])
    reps = IntegerField('Number of Repetitions:',validators=[DataRequired()])
    weight = IntegerField('Weight')

class ExerciseForm(BaseForm):
     name = StringField('Name',validators=[DataRequired()])
     category = QuerySelectField('Category',query_factory=lambda: Category.query.all())
     muscles_used = QuerySelectMultipleField('Muscles Used:', query_factory=lambda: Muscle.query.all(),widget=widgets.ListWidget(prefix_label=False),option_widget=widgets.CheckboxInput())
     equipment = QuerySelectMultipleField('Equipment:', query_factory=lambda: Equipment.query.all(),widget=widgets.ListWidget(prefix_label=False),option_widget=widgets.CheckboxInput())
     description = TextAreaField('Description:')

class SignUp(BaseForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])

class LoginForm(BaseForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8)])

class WeightEntryForm(BaseForm):
    date = DateField("Date",default=date.today)
    weight = IntegerField("Weight(lbs)",validators=[DataRequired()])

class OneRepMaxForm(BaseForm):
    repetitions = IntegerField("Number of Repetitions", validators=[DataRequired()])
    weight_lifted = IntegerField("Weight(lbs)", validators=[DataRequired()])











