from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

from datetime import datetime

from flask_bcrypt import Bcrypt






db = SQLAlchemy()

metadata = MetaData()

### User Models ###

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    weight_entries = db.relationship('WeightEntry', backref='user')
    workouts = db.relationship('Workout', backref='user')

    def __repr__(self):
        return f"<User #{self.id}: {self.name}, {self.username}, {self.email}, {self.weight_entries}, {self.workouts}>"


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
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

### Workout Models ###

class Workout(db.Model):

    __tablename__ = 'workout'

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    sets = db.relationship('Set', backref='workout')
    time = db.Column(db.Integer)

class Set(db.Model):

    __tablename__ = 'set'

    id = db.Column(db.Integer, primary_key=True)
    exercise = db.relationship('Exercise', backref='set',lazy=True)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    workout_id = db.Column(db.Integer,db.ForeignKey('workout.id'))



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
    

    def __repr__(self):
        return f"<Muscle #{self.id}, {self.name}"

class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercise',backref='category',lazy=True)
    
    def __repr__(self):
        return f"<Category #{self.id},{self.name}, {self.exercises}>"

class Equipment(db.Model):

    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    exercises = db.relationship('Exercise',secondary=equipment_exercises)

    def __repr__(self):
        return f"<Equipment #{self.id},{self.name},{self.exercises}"



    
class Exercise(db.Model):

    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    set_id = db.Column(db.Integer, db.ForeignKey('set.id'))
    muscles = db.relationship('Muscle',secondary=muscles_used)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Exercise #{self.id},{self.name},{self.muscles},{self.description}"
    

    


    

#### Association Tables ####






   

def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)   



