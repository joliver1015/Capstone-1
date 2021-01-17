import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, WeightEntry, Workout, Set

os.environ['DATABASE_URL'] = "postgresql:///exercise_api-test"

from app import app

db.create_all

class ExerciseModelTestCase(TestCase):
    
    """ Test for Exercise """

    def setUp(self):
        """Create test client, add sample data"""
        db.drop_all()
        db.create_all()

        self.exerciseid = 100
        ex = Exercise("test","testcategory","testmuscles","testequipment","testdescription")
        ex.id = self.exerciseid
        db.session.commit()

        self.ex = Exercise.query.get(self.exerciseid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_exercise_model(self):
        """ Does basic model work? """

        testcat = Category(name="testcat")

        testmuscle1 = Muscle(name="test1")
        testmuscle2 = Muscle(name="test2")
        testequipment1 = Equipment(name="equip1")
        testequipment2 = Equipment(name="equip2")



        ex = Exercise(
            name = "test"
            category = testcat
            muscles = [testmuscle1,testmuscle2]
            equipment = [testequipment1,testequipment2]
            description = "testdescription"
        )

        testcat.exercises.append(ex)
        testmuscle1.exercises.append(ex)
        testmuscle2.exercises.append(ex)
        testequipment1.exercises.append(ex)
        testequipment2.exercises.append(ex)

        db.session.commit()

        self.assertEquals(len(testcat.exercises),1)
        self.assertEquals(len(testmuscle1.exercises),1)
        self.assertEquals(len(testmuscle2.exercises),1)
        self.assertEquals(len(testequipment1.exercises),1)
        self.assertEquals(len(testequipment2.exercises),1)

        