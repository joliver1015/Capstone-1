from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

from datetime import datetime

from flask_bcrypt import Bcrypt






db = SQLAlchemy()


metadata = MetaData()

bcrypt = Bcrypt()



### User Models ###

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    workouts = db.relationship("Workout", cascade="all, delete")
    weight_entries = db.relationship("WeightEntry", cascade="all, delete")

    def __repr__(self):
        return f"<User # {self.id}: {self.username}>"

    @classmethod
    def register(cls,username,pwd):

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)

    
    @classmethod
    def authenticate(cls,username,password):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):

            return u
        else:
            return False
        
        



class WeightEntry(db.Model):
    
    __tablename__ = 'weight_entry'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    



 


### Workout Models ###

class Workout(db.Model):

    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    sets = db.relationship('Set', backref='workout_sets',lazy='dynamic',cascade="all, delete")
    time = db.Column(db.Integer)

    


       




class Set(db.Model):

    __tablename__ = 'set'

    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(20))
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    workoutid = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    workout = db.relationship('Workout',backref='workout_sets')



### Exercise Models ###
muscles_used = db.Table('muscles_used',db.Model.metadata,
            db.Column('exercise_id',db.Integer, db.ForeignKey('exercise.id')),
            db.Column('muscle_id',db.Integer, db.ForeignKey('muscle.id'))
        )

equipment_exercises = db.Table('equipment_exercises', db.Model.metadata,
                    db.Column('equipment_id',db.Integer,db.ForeignKey('equipment.id')),
                    db.Column('exercise_id',db.Integer,db.ForeignKey('exercise.id'))
                )

class Muscle(db.Model):

    __tablename__ = 'muscle'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False)
    exercises = db.relationship('Exercise', secondary="muscles_used",back_populates="muscles")

    def __repr__(self):
        return f"{self.name}"

class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercise',backref='category')
    
    def __repr__(self):
        return f"{self.name}"

class Equipment(db.Model):

    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercise',secondary=equipment_exercises, back_populates="equipment")

    def __repr__(self):
        return f"{self.name}"



    
class Exercise(db.Model):

    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    set_id = db.Column(db.Integer, db.ForeignKey('set.id'))
    muscles = db.relationship('Muscle',secondary=muscles_used, back_populates="exercises")
    equipment = db.relationship('Equipment', secondary=equipment_exercises, back_populates="exercises")
    description = db.Column(db.Text)

    def __repr__(self):
        return f"{self.name}"
    
   

def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)   



