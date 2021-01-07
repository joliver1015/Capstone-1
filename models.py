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

    def get_latest_entry(self,user):
        last_entries = WeightEntry.objects.filter(user_id=user.id).order_by('-date')[:5]
        last_entries_details = []

        for index, entry in enumerate(last_entries):
            curr_entry = entry
            prev_entry_index = index + 1

            if prev_entry_index < len(last_entries):
                prev_entry = last_entries[prev_entry_index]
                else:
                    prev_entry = None
            if prev_entry and curr_entry:
                weight_diff = curr_entry.weight - prev_entry.weight
            else:
                weight_diff = None
            last_entries_details.append((curr_entry, weight_diff))
        return last_entries_details


### Workout Models ###

class Workout(db.Model):

    __tablename__ = 'workout'

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    sets = db.relationship('Set', backref='workout')
    time = db.Column(db.Integer)

    def get_latest_workout(self,user):
        last_workout = Workout.objects.filter(user=user).order_by('date').last()
        if last_workout:
            return last_workout
        else:
            return None
       




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
        return f"<{self.name}>"

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
        return f"<{self.name}>"
    

    

   

def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)   



