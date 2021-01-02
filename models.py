from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from flask_bcrypt import Bcrypt


db = SQLAlchemy()



### User Models ###

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.COlumn(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    weight_entries = db.relationship('WeightEntry')
    workouts = db.relationship('Workout')


    @classmethod
    def signup(cls, username, email, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username = username,
            email = email,
            password = hashed_pwd
        )
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls,username,password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user



class WeightEntry(db.Model):
    
    __tablename__ = 'weight_entry'
    
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

### Workout Models ###

class Workout(db.Model):

    __tablename__ = 'workout'

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    sets = db.relationship('Set')
    time = db.Column(db.Time)

class Set(db.Model):

    __tablename__ = 'set'

    exercise = db.relationship(db.Integer, db.ForeignKey('exercise.id'))
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    workout_id = db.Column(db.Integer,db.ForeignKey('workout.id'))


### Exercise Models ###


class Exercise(db.Model):

    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text, nullable=False)
    muscles = db.relationship('Muscle')
    category = db.Column(db.ForeignKey('category.id'))
    equipment = db.Column(db.ForeignKey('equipment.id'))
    description = db.Column(db.Text)

class Muscle(db.Model):

    __tablename__ = 'muscle'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False)
    exercise = db.Column(db.ForeignKey('exercise.id'))

class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercise')

class Equipment(db.Model):

    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercise')










        




    

def connect_db(app):
    db.app = app
    db.init_app(app)