from models import *

from app import db


def seed_data():

    db.drop_all()

    db.create_all()

########################
#Categories

    arms = Category(name="Arms")
    abdominal = Category(name="Abs")
    back = Category(name="Back")
    calves = Category(name="Calves")
    chest = Category(name="Chest")
    legs = Category(name="Legs")
    shoulders = Category(name="Shoulders")

    db.session.add(arms)
    db.session.add(abdominal)
    db.session.add(back)
    db.session.add(calves)
    db.session.add(chest)
    db.session.add(legs)
    db.session.add(shoulders)
    db.session.commit()


    ##########################
    # Equipment

    barbell = Equipment(name="Barbell")
    bodyweight = Equipment(name="Bodyweight")
    dumbbell = Equipment(name="Dumbbell")
    ez_bar = Equipment(name="EZ Bar")
    machine = Equipment(name="Machine")
    pullup_bar = Equipment(name="Pull-up Bar")
    resist_band = Equipment(name="Resistance Band")
    swiss_ball = Equipment(name="Swiss Ball")
    trx = Equipment(name="TRX")

    db.session.add(barbell)
    db.session.add(bodyweight)
    db.session.add(dumbbell)
    db.session.add(ez_bar)
    db.session.add(machine)
    db.session.add(pullup_bar)
    db.session.add(resist_band)
    db.session.add(swiss_ball)
    db.session.add(trx)

    db.session.commit()

    ##################################################
    # Muscles

    anterior_deltoid = Muscle(name="Anterior deltoid")
    biceps_brachii = Muscle(name="Biceps brachii")
    biceps_femoris = Muscle(name="Biceps femoris")
    brachialis = Muscle(name="Brachialis")
    gastroc = Muscle(name="Gastrocnemius")
    glute_max = Muscle(name="Gluteus maximus")
    lateral_deltoid = Muscle(name="Lateral deltoid")
    lat_dorsi = Muscle(name="Latissimus dorsi")
    obliquus = Muscle(name="Obliquus externus abdominis")
    pec_major = Muscle(name="Pectoralis major")
    pec_minor = Muscle(name="Pectoralis minor")
    post_deltoid = Muscle(name="Posterior deltoid")
    quads = Muscle(name="Quadriceps femoris")
    rectus_ab = Muscle(name="Rectus abdominus")
    serratus_anterior = Muscle(name="Serratus anterior")
    soleus = Muscle(name="Soleus")
    traps = Muscle(name="Trapzius")
    triceps = Muscle(name="Triceps brachii")

    db.session.add(anterior_deltoid)
    db.session.add(biceps_brachii)
    db.session.add(biceps_femoris)
    db.session.add(brachialis)
    db.session.add(gastroc)
    db.session.add(glute_max)
    db.session.add(lateral_deltoid)
    db.session.add(lat_dorsi)
    db.session.add(obliquus)
    db.session.add(pec_major)
    db.session.add(pec_minor)
    db.session.add(post_deltoid)
    db.session.add(quads)
    db.session.add(rectus_ab)
    db.session.add(serratus_anterior)
    db.session.add(soleus)
    db.session.add(traps)
    db.session.add(triceps)

    db.session.commit()

    ###########################################
    # Exercises
    


