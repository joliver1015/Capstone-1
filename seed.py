from models import *
from app import app


weight = [180]

muscle_1 = 'Pectoralis Major'
muscle_2 = 'Triceps Brachii'
muscles_worked = [muscle_1,muscle_2]
category = 'Chest'
equipment = 'Barbell'


db.drop_all()
db.create_all()

test_user = User(name='James',username='joliver',email='joliver@test.com',password='secret')
test_weight_entry = WeightEntry(date='2021-01-04',weight=180.4)
test_workout = Workout(name="Chest Day",date='2021-01-04',time=90)
test_set = Set(reps=10,weight=135)

test_equipment = Equipment(name=equipment)
test_category = Category(name=category)
test_exercise = Exercise(name="Bench Press",category_id=test_category.id,description="Lower bar to chest...")
test_muscle = Muscle(name=muscle_1)
test_workout.sets.append(test_set)
test_exercise.muscles.append(test_muscle)
test_equipment.exercises.append(test_exercise)

test_category.exercises.append(test_exercise)

test_set.exercise.append(test_exercise)

test_user.workouts.append(test_workout)
test_user.weight_entries.append(test_weight_entry)

db.session.add(test_category)
db.session.add(test_equipment)
db.session.add(test_user)

db.session.commit()

print(Category.query.get(1))
print(Exercise.query.get(1))
print(Equipment.query.get(1))
print(User.query.get(1))