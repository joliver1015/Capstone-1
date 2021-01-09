from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
from forms import *

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/exercise_api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Secret_150%'
migrate = Migrate(app, db)

connect_db(app)

#######################################################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """ If logged in, add curr user to Global Flask"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None
    
def do_login(user):
    """ Log in user. """
    session[CURR_USER_KEY] = user.id  

def do_logout():
    """ Logout user. """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    

@app.route('/signup', methods=["GET","POST"])
def signup():
    """ Handle user signup.

    Creates new user and add to DB. Redirect to user dashboard.

    Redirects user to form if there is already a user with that username. 
    """

    form = SignUp()

    if form.validate_on_submit():
        try:
            user = User.signup(
                name = form.name.data,
                username = form.name.data,
                email=form.email.data,
                password = form.password.data,
            )

        except IntegrityError:
            flash("username already taken",'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html'form=form)

@app.route('/logout')
def logout():
    """Handle logout of user"""

    do_logout()
    flask("You have successfully logged out")

    return redirect("/")

############## Workout Routes #######################

@app.route('/workout/<int:workout.id>',methods=["GET"])
def show_workout(workout_id):
    """ Show workout details"""
    
    user = g.user

    workout = user.workouts.query.get_or_404(workout_id)

    return render_template('users/workout.html', user=user, workout=workout)

@app.route('/workout/new', methods=["GET","POST"])
def add_workout():
    """ Add a workout

    Show form if GET. If valid adds workout to user and redirects to workout page to add sets """

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")
    
    form = WorkoutForm()

    if form.validate_on_submit():
        wo = Workout(name=form.name.data,date=form.date.data,time=form.time.data)
        g.user.workouts.append(wo)
        db.session.commit()

        return redirect(f"/workout/{wo.id}")
    
    return render_template('workout/new.html', form=form)

@app.route('/workout/<int:workout.id>/set/new'methods=["GET","POST"])
def add_set(workout_id):

    if not g.user:
        flash("Access unauthorized", "danger")
        return("/")
    
    workout = g.user.workouts.query.get_or_404(workout_id)
    
    form = SetForm()

    if form.validate_on_submit():
        workout_set = Set(exercise=form.exercise.data,reps=form.reps.data,weight=form.weight.data)
        workout.sets.append(workout_set)
        db.session.commit()
    
        return redirect(f'/workout/{workout_id}')
    
    return render_template('workout/new-workout.html', form=form)
    

############### Weight Entry Routes ####################

@app.route('/weight-entries/all',methods=["GET"])
def show_all_entries(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("/users/weight-entries",user=user, weight_entries=user.weight_entries)

@app.route('/weight-entries/new',methods=["GET","POST"])
def add_weight_entry():

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/")
    
    form = WeightEntryForm()

    if form.validate_on_submit():
        entry = WeightEntry(date=form.date.data,weight=form.weight.data)
        g.user.weight_entries.append(entry)
        db.session.commit()

        return redirect(f'/weight-entries/all')
    
    return render_template('weight-entries/new-weight.html', form=form)

#################### Exercise Routes ################################

@app.route('/exercises/overview', methods=["GET"])
def show_all_exercises():

    """ Shows all exercises alphabetically"""

    exercises = Exercise.query.order_by(exercise.name)

return render_template("exercise/all.html", exercises=exercises)

@app.route('/exercises/new', methods=["GET","POST"])
def add_exercise():

    """ Adds new exercise if logged in as user """

    if not g.user:
        flash("Access unauthorized","danger")
        return redirect("/")
    
    form = ExerciseForm()

    if form.validate_on_submit():
        new_exercise = Exercise(name=form.name.data,category=form.category.data,muscles_used=form.muscles_used.data,description=form.description.data)
        form.category.data.append(new_exercise)
        db.session.commit()

        return redirect(f'/exercises/all')
    
    render_template("exercise/new.html", form=form)

@app.route('/exercises/categories/overview',methods=["GET"])
def show_all_categories():

    """ Shows exercise categories alphabetically  """

    categories = Category.query.order_by(category.name)

    return render_template("/exercises/categories/overview.html", categories=categories)

@app.route('/exercises/muscles/overview', methods=["GET"])
def show_all_muscles():

    """ Shows muscles alphabetically """

    muscles = Muscle.query.order_by(muscle.name)

    return render_template("exercise/muscles/overview.html", muscles=muscles)

@app.route('/exercises/categories/<int:category.id>/view', methods=["GET"])
def exercises_by_category(category_id):

    """ Shows exercises by category """

    category = Category.query.get_or_404(category_id)

    return render_template("exercise/categories/view.html", category=category)

@app.route('/exercises/muscles/<int:muscle.id>/view/<str:muscle.name>', methods=["GET"])
def exercises_by_muscles(muscle_id):
    
    """ Shows exercises by muscle """

    exercises = Exercise.query.filter(muscles_used.id=muscle_id)

    return render_template("exercise/muscles/view.html", exercises=exercises)






    










    
















