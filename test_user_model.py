import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, WeightEntry, Workout, Set

os.environ['DATABASE_URL'] = "postgresql:///exercise_api-test"

from app import app

db.create_all

class UserModelTestCase(TestCase):

    def setUp(self):
        """ Create test client, add sample data """
        db.drop_all()
        db.create_all()

        u = User.register("test","password")
        uid = 1111
        u.id = uid1

        db.session.commit()

        self.u = u
        self.uid = uid

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_user_model(self):
        """Does user model work? """

        u = User(username="testuser", password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        # User should not have any workouts or weights logged
        self.assertEqual(len(u.workouts), 0)
        self.assertEqual(len(u.weight_entries), 0)
    
    def test_user_workout(self):
        """Does workout get added to user? Then does a set get added to workout?"""

        test_workout = Workout(
            name = "test",
            date = "2021-01-01",
            time = 60
        )

        self.u.workouts.append(test_workout)

        db.session.commit()

        self.assertEqual(len(self.u.workouts), 1)

        test_set = Set(
            exercise="test_exercise",
            reps = 10,
            weight = 150,
            workoutid = test_workout.id
        )

        test_workout.sets.append(test_set)
        db.session.commit()

        self.assertEqual(len(self.u.workouts.sets), 1)

    
    def test_user_weight_log(self):

        """ Does weight entry get added to user's log? """

        test_weight = WeightEntry(
            date = "2021-01-01"
            weight = 180
            user_id = self.uid
        )

        self.u.weight_entries.append(test_weight)
        db.session.commit()

        self.assertEqual(len(self.u.weight_entries), 1)

    ############################################################
    # Sign up Tests

    def test_valid_signup(self):
        u_test = User.register("testtest","password")
        uid = 1010
        u_test.id = uid
        db.session.commit

        u_test = User.query.get(uid)

        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username,"testtest")
        self.assertEqual(u_test.password, "password")
        self.assertTrue(u_test.password.startswith("$2b$"))

    
    def test_invalid_username_signup(self):
        invalid = User.register(None,"password")
        uid = 2020
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
        
    def test_invalid_password_signup(self):
        invalid = User.register("test",None)
        uid = 2019
        invalid.id = uid
        with self.assertRaises(ValueError) as context:
            db.session.commit()
    
    ####################################################################
    # Authenticate Tests

    def test_valid_authentication(self):
        u = User.authenticate(self.u.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername","password"))
    
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u.username,"badpassword"))
    

        


    
    




