from flask import Flask, render_template, redirect, request, flash, g, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from models import db, connect_db, User, WeightEntry, Workout, Set, Exercise, Category, Muscle, Equipment
from sqlalchemy.types import Text
from forms import *
from seed import seed_data

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/exercise_api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '20930485093202934'

connect_db(app)

app.app_context().push()

#Uncomment this and comment out the db.create_all() below to load initial data. WARNING: This will clear user data
#seed_data()


db.create_all()

#######################################################################################################
# User signup/login/logout
@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):

    session[CURR_USER_KEY] = user.id  

def do_logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET","POST"])
def signup():

    """ Shows registration page and form """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    

    form = SignUp()

    if form.validate_on_submit():

        username = form.username.data  
        pwd = form.password.data

        user = User.register(username,pwd)
        db.session.add(user)
        
        db.session.commit()

        do_login(user)
       
        

        return redirect('/dashboard')
    
    return render_template("users/signup.html", form=form)
        
    


@app.route('/login',methods=["GET","POST"])
def login():

    """ Shows log-in page """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            do_login(user)
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            
            return redirect('/dashboard')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('users/login.html', form=form)
   

@app.route('/logout')
def logout_user():
    do_logout()
    return redirect('/')

################################################
# Other User actions:

@app.route('/user/settings',methods=["GET"])
def user_settings():

    """ Show user settings page"""

    if not g.user:
        if "user_id" not in session:
            flash("You must be logged in to view this page")
            return redirect("/")
    
    return render_template("users/settings.html")

@app.route('/user/edit')
def user_edit():
    user = g.user

    if not g.user:
        if "user_id" not in session:
            flash("You must be logged in to view this page")
            return redirect("/")
    
    form = SignUp()

    if form.validate_on_submit():
        
        user.username = form.username.data
        user.password = form.password.data
    
        db.session.commit()
        return redirect(f"/users/settings")
    
    render_template(f"/users/edit", form=form)

@app.route('/user/delete', methods=["POST"])
def delete_user():

    """ Delete User"""

    if not g.user:
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")
    
    
    
    do_logout()

    
    
    db.session.delete(g.user)
    db.session.commit()

    return redirect('/signup')

################################################
# Homepage and dashboard

@app.route('/')
def show_welcome():
    """ Shows home page to users not logged in """
    if g.user:
        return redirect('/dashboard')
    return render_template("home.html")

@app.route('/dashboard', methods=["GET"])
def dashboard():

    """ Shows user's dashboard as home page if user is logged in"""

    if "user_id" not in session:
        return redirect("/")
    
    else:

        if g.user.workouts:
            latest_workout = g.user.workouts[-1]
        
        else:
            latest_workout= None
        
        if g.user.weight_entries:
            curr_entry = g.user.weight_entries[-1]
            prev_entry = g.user.weight_entries[0]
            weight_diff = curr_entry.weight - prev_entry.weight
        else:
            curr_entry = None
            prev_entry = None
            weight_diff = None


        return render_template("dashboard.html", current_weight=curr_entry, weight_diff=weight_diff,latest_workout=latest_workout)

@app.route('/unauthorized',methods=["GET"])
def show_unauthorized_page():

    """ Shows page for users not logged in trying to access account-only features """

    return render_template("unauthorized.html")

##################################################
#Workout Routes

@app.route('/workout/overview',methods=["GET"])
def show_all_workouts():

    """ Shows all of a user's workouts """

    if not g.user:
        flash("You must be logged in to view this page")
        return redirect("/unauthorized")
    
    else:

        all_workouts = g.user.workouts

        return render_template("workout/overview.html", workouts=all_workouts)


@app.route('/workout/view/<workout_id>',methods=["GET"])
def view_workout(workout_id):

    """ Shows specific workout details """

    if  not g.user:
        flash("You must be logged in to view this page")
        return redirect("/unauthorized")

    else:
        workout = Workout.query.get_or_404(workout_id)
    

        form = SetForm()
       

            

    return render_template("workout/detail.html",form=form, workout=workout)
    

@app.route('/workout/new',methods=["GET","POST"])
def new_workout():

    """ Page for creating a new workout """

    if  not g.user:
        return redirect("/unauthorized")
    
    else:

        form = WorkoutForm()
    
        if form.validate_on_submit():

            new_workout = Workout(
                name = form.name.data,   
                date = form.date.data,   
                time = form.time.data,
                user_id = g.user.id
            )
            
            g.user.workouts.append(new_workout)
            db.session.commit()
            return redirect(url_for('view_workout',workout_id=new_workout.id))
    
    return render_template("workout/new.html",form=form)

######################################################################################
# Set Routes

@app.route('/workout/<workout_id>/new-set', methods=["POST"])
def new_set(workout_id):

    """ Creates a new set on the workout page """


    workout = Workout.query.get_or_404(workout_id)

    form = SetForm()

    if form.validate_on_submit():

        new_set = Set(
            exercise = form.exercise.data,   
            reps = form.reps.data,
            weight = form.weight.data,
            workoutid = workout_id
        )

        workout.sets.append(new_set)
        db.session.commit()
        return redirect(url_for('view_workout',workout_id=workout_id))
    
    return render_template('workout/new-set.html', form = form)

@app.route('/workout/<workout_id>/<set_id>/delete-set' methods=["POST"])
def delete_set(workout_id,set_id):

    workout = Workout.query.get_or_404(workout_id)

    target_set = workout.sets.set_id

    workout.sets.remove(target_set)

    db.session.commit()

    return redirect(url_for('view_workout',workout_id=workout_id))


#####################################################################################
# Weight entry routes

@app.route('/weightentries/overview', methods=["GET"])
def all_weight_entries():

    """ Shows the user's entire weight log """

    if not g.user:
        flash("You must be logged in to view this page")
        return redirect("/unauthorized")
    
    else:

        all_weight_entries = g.user.weight_entries 
    
    return render_template("weight-entries/all.html", weight_entries = all_weight_entries)


@app.route('/weightentries/new', methods=["GET","POST"])
def new_entry():

    """ Page for adding a new weight entry """

    if not g.user:
        flash("You must be logged in to view this page")
        return redirect("/unauthorized")
    
    else:

        form = WeightEntryForm()

        if form.validate_on_submit():

            new_weight_log = WeightEntry(
               date = form.date.data,   
               weight = form.weight.data,
               user_id = g.user.id 
            )

            g.user.weight_entries.append(new_weight_log)
            db.session.commit()
            return redirect('/weightentries/overview')
    
    return render_template("weight-entries/new-weight.html", form=form)





#################################################################################
#Exercise Routes

@app.route('/exercise/overview',methods=["GET"])
def show_all_exercises():

    """ Page for showing all exercises """

    all_exercises = Exercise.query.all()

    return render_template("exercise/all.html", exercises=all_exercises)

@app.route('/exercise/<exercise_id>/view',methods=["GET"])
def view_exercise(exercise_id):

    exercise = Exercise.query.get_or_404(exercise_id)

    return render_template("exercise/detail.html", exercise=exercise)


@app.route('/exercise/new',methods=["GET","POST"])
def create_exercise():

    """ Page for creating a new exercise """

    if not g.user:
        flash("You must be logged in to view this page")
        return redirect("/unauthorized")
    
    else:
        form = ExerciseForm()

        if form.validate_on_submit():

            new_exercise = Exercise(
                name = form.name.data,
                category = form.category.data,
                muscles = form.muscles_used.data,   
                equipment = form.equipment.data,
                description = form.description.data
            )
                
            category = form.category.data
            equipment = form.equipment.data
            muscles = form.muscles_used.data

            category.exercises.append(new_exercise)


            for equip in equipment:
                equip.exercises.append(new_exercise)
            
            for muscle in muscles:
                muscle.exercises.append(new_exercise)    
            
            db.session.commit()
            return redirect(url_for("show_all_exercises"))
    
    return render_template("exercise/new.html", form=form)

@app.route('/exercise/<exercise_id>/delete',methods=["POST"])
def delete_exercise(exercise_id):

    """ Deletes an exercise from the database """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/unauthorized")
    
    exercise = Exercise.query.get(exercise_id)
    db.session.delete(exercise)
    db.session.commit()

    return redirect(url_for("show_all_exercises"))

#################################################################
#Exercise Categories

@app.route('/exercise/categories/overview',methods=["GET"])
def view_all_categories():

    """ Shows all exercise categories """

    all_categories = Category.query.all()

    return render_template("exercise/categories/overview.html", categories = all_categories)

@app.route('/exercise/categories/<category_id>/view', methods=["GET"])
def view_category(category_id):

    """ Shows exercises related to specific category """

    category = Category.query.get_or_404(category_id)

    return render_template("exercise/categories/view.html", category=category)

#########################################################################
#Muscle Routes


@app.route('/exercise/muscles/overview', methods=["GET"])
def show_all_muscles():

    """ Shows all muscles in database """

    all_muscles = Muscle.query.all()

    return render_template("exercise/muscles/overview.html", muscles = all_muscles)

@app.route('/exercise/muscles/<muscle_id>/view',methods=["GET"])
def view_muscle_exercises(muscle_id):

    """ Shows all exercises used by specfic muscle """

    muscle = Muscle.query.get_or_404(muscle_id)

    return render_template("exercise/muscles/view.html", muscle= muscle)

############################################################################################
#Equipment Routes

@app.route('/exercise/equipment/overview', methods=["GET"])
def show_all_equipment():

    """ Shows all exercise equipment """

    all_equipment = Equipment.query.all()

    return render_template("exercise/equipment/overview.html", equipment=all_equipment)

@app.route('/exercise/equipment/<equipment_id>/view', methods=["GET"])
def view_equipment_exercises(equipment_id):

    """ Shows all exercises that use specfic equipment """

    equipment = Equipment.query.get(equipment_id)

    return render_template("exercise/equipment/view.html", equipment=equipment)









    








    










    
















