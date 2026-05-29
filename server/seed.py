#!/usr/bin/env python3

from app import app, db
from models import Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding Exercises...")
    squat = Exercise(name="Barbell Squat", category="Legs", equipment_needed=True)
    pushup = Exercise(name="Push Up", category="Chest", equipment_needed=False)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)
    
    db.session.add_all([squat, pushup, plank])
    db.session.commit()

    print("Seeding Workouts...")
    w1 = Workout(date=date(2023, 10, 1), duration_minutes=60, notes="Felt great!")
    w2 = Workout(date=date(2023, 10, 3), duration_minutes=45, notes="Quick core and chest day.")
    
    db.session.add_all([w1, w2])
    db.session.commit()

    print("Seeding Workout Exercises (Join Table)...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, reps=10, sets=3)
    we2 = WorkoutExercise(workout_id=w2.id, exercise_id=pushup.id, reps=15, sets=4)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=plank.id, duration_seconds=60, sets=3)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete!")