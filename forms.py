from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length
from Datetime import date
from wtforms_sqlalchemy.fields import QuerySelectField


class WorkoutForm(FlaskForm):

    workout_name = StringField('Workout Name', validators=[DataRequired()])
    date = DateField('Workout Date', default=date.today))
    time = IntegerField('Time Elapsed(min)')

class SetForm(FlaskForm):
    exercise = QuerySelectField('Exercise',query_factory=exercise_query, allow_blank=True, get_label='name')
    reps = IntegerField('Number of Repetitions:',validators=[DataRequired()])
    weight = IntegerField('Weight')

class ExerciseForm(FlaskForm):
     name = StringField('Name',validators=[DataRequired()])
     category = QuerySelectField('Category',query_factory=category_query(),allow_blank=False,get_label='name')
     muscles_used = QuerySelectField('Muscles Used:',query_factory=muscle_query(), allow_blank=True, get_label='name')
     description = TextAreaField('Description:')

class SignUp(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])

class Login(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8)])




def exercise_query():
    return Exercise.query

def category_query():
    return Category.query

def muscle_query():
    return Muscle.query
    

