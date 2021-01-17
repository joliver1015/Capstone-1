from models import *



db.drop_all()

db.create_all()

######################
#Categories

abdominal = Category(name="Abs")
arms = Category(name="Arms")
back = Category(name="Back")
calves = Category(name="Calves")
chest = Category(name="Chest")
legs = Category(name="Legs")
shoulders = Caregory(name="Shoulders")

db.session.add(arms,back,calves,chest,legs, shoulders)
db.session.commit()

