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
    
    deadlift = Exercise(name="Deadlift", category_id=3,muscles=[lat_dorsi,quads,glute_max],equipment=[barbell,dumbbell,machine],description="Stand with feet shoulder width apart, hips hinged out with knees bent as needed to reach bar.While squeezing shoulder blades and glutes, lift bar till hips lock out. Safely lower bar to ground maintaining posture.")
    bench_press = Exercise(name="Bench Press",category_id=5,muscles=[pec_major,pec_minor,serratus_anterior,triceps],equipment=[barbell,dumbbell,machine],description="Hold bar with arms shoulder width apart. Lower bar/dumbbells to chest. While keeping head, hips, and feet planted on the bench and floor, Lift until arms lockout. If using dumbbells, be sure to raise arms directly over shoulders for optimal pectoral muscle activation.")
    back_squat = Exercise(name="Back Squat",category_id=6,muscles=[quads, glute_max, gastroc, soleus, biceps_femoris],equipment=[barbell],description="Stand with feet shoulder width apart, squeeze shoulder blades to form area for bar to rest. Lower till legs are parallet with floor. When lifting up, maintain straight back and keep knees from turning inwards.")
    military_press = Exercise(name="Military Press",category_id=7,muscles=[anterior_deltoid,lateral_deltoid],equipment=[barbell,dumbbell,machine,resist_band],description="Start with weight at shoulder level. Lift up until arms lockout, making sure not to bend back")
    sit_ups = Exercise(name="Sit ups",category_id=2,muscles=[rectus_ab,obliquus],equipment=[bodyweight,swiss_ball],description="Lay flat on floor with knees bent. Lift torso, putting emphasis on squeezing the ab region to ensure activation")
    rows = Exercise(name="Rows",category_id=3,muscles=[traps,biceps_brachii,post_deltoid],equipment=[barbell,dumbbell,resist_band,machine,trx], description="Start with arms straight, retract shoulders blades while lifting to ensure proper muscle activation")
    bicep_curl = Exercise(name="Bicep Curl",category_id=1,muscles=[biceps_brachii,brachialis],equipment=[barbell,dumbbell,ez_bar,trx],description="Begin with arms straight, lift at elbows,keeping back straight")
    calf_raises = Exercise(name="Calf Raises",category_id=4,muscles=[gastroc,soleus],equipment=[barbell,dumbbell,machine],description="With weight on shoulders, raise heels,to activate soleus, bend at the knees.")
    skull_crushers = Exercise(name="Skullcrushers",category_id=1,muscles=[triceps],equipment=[barbell,dumbbell,ez_bar], description="Laying flat on bench or floor, starting with arms straight, bend at elbow towards head, keeping elbows parallel with body")
    pull_ups = Exercise(name="Pull-ups",category_id=3,muscles=[lat_dorsi,post_deltoid,traps,biceps_brachii],equipment=[pullup_bar],description="Hold bar with shoulder width grip, palms facing away. Retract shoulder blades and pull up till chin is over bar.Lower till just before shoulder lockout.")
    roll_outs = Exercise(name="Rollouts",category_id=2,muscles=[rectus_ab,obliquus],equipment=[swiss_ball],description="Keeping back straight with forearms on ball,lower hips towards the floor, arms reaching out away from body. Raise torso back to starting position keeping back straight and hips level.")

    back.exercises.append(deadlift)
    back.exercises.append(rows)
    chest.exercises.append(bench_press)
    legs.exercises.append(back_squat)
    calves.exercises.append(calf_raises)
    arms.exercises.append(bicep_curl)
    arms.exercises.append(skull_crushers)
    abdominal.exercises.append(sit_ups)
    shoulders.exercises.append(military_press)
    abdominal.exercises.append(roll_outs)
    back.exercises.append(pull_ups)

    lat_dorsi.exercises.append(deadlift)
    quads.exercises.append(deadlift)
    glute_max.exercises.append(deadlift)

    pec_major.exercises.append(bench_press)
    pec_minor.exercises.append(bench_press)
    serratus_anterior.exercises.append(bench_press)
    triceps.exercises.append(bench_press)

    quads.exercises.append(back_squat)
    glute_max.exercises.append(back_squat)
    biceps_femoris.exercises.append(back_squat)
    gastroc.exercises.append(back_squat)
    soleus.exercises.append(back_squat)

    anterior_deltoid.exercises.append(military_press)
    lateral_deltoid.exercises.append(military_press)

    rectus_ab.exercises.append(sit_ups)
    obliquus.exercises.append(sit_ups)

    traps.exercises.append(rows)
    post_deltoid.exercises.append(rows)
    biceps_brachii.exercises.append(rows)

    biceps_brachii.exercises.append(bicep_curl)
    brachialis.exercises.append(bicep_curl)

    gastroc.exercises.append(calf_raises)
    soleus.exercises.append(calf_raises)

    triceps.exercises.append(skull_crushers)

    lat_dorsi.exercises.append(pull_ups)
    post_deltoid.exercises.append(pull_ups)
    traps.exercises.append(pull_ups)
    biceps_brachii.exercises.append(pull_ups)

    rectus_ab.exercises.append(roll_outs)
    obliquus.exercises.append(roll_outs)

    machine.exercises.append(deadlift)
    machine.exercises.append(bench_press)
    machine.exercises.append(calf_raises)
    machine.exercises.append(military_press)
    machine.exercises.append(rows)
    
    barbell.exercises.append(deadlift)
    barbell.exercises.append(bench_press)
    barbell.exercises.append(back_squat)
    barbell.exercises.append(military_press)
    barbell.exercises.append(bicep_curl)
    barbell.exercises.append(skull_crushers)
    barbell.exercises.append(calf_raises)
    barbell.exercises.append(rows)

    dumbbell.exercises.append(deadlift)
    dumbbell.exercises.append(bench_press)
    dumbbell.exercises.append(military_press)
    dumbbell.exercises.append(bicep_curl)
    dumbbell.exercises.append(calf_raises)
    dumbbell.exercises.append(skull_crushers)
    dumbbell.exercises.append(rows)

    bodyweight.exercises.append(sit_ups)

    trx.exercises.append(bicep_curl)

    ez_bar.exercises.append(bicep_curl)
    ez_bar.exercises.append(skull_crushers)

    pullup_bar.exercises.append(pull_ups)

    swiss_ball.exercises.append(sit_ups)
    swiss_ball.exercises.append(roll_outs)

    


    db.session.commit()
