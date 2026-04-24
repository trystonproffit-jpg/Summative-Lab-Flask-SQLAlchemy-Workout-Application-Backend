#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing database...")

    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()

    print("Creating exercises...")

    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    treadmill = Exercise(
        name="Treadmill Run",
        category="Cardio",
        equipment_needed=True
    )

    print("Creating workouts...")

    workout1 = Workout(
        date=date(2026, 4, 24),
        duration_minutes=45,
        notes="Full body workout"
    )

    workout2 = Workout(
        date=date(2026, 4, 25),
        duration_minutes=30,
        notes="Quick cardio session"
    )

    db.session.add_all([pushups, squats, treadmill, workout1, workout2])
    db.session.commit()

    print("Adding exercises to workouts...")

    we1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        sets=3,
        reps=15
    )

    we2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=squats.id,
        sets=4,
        reps=12
    )

    we3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=treadmill.id,
        duration_seconds=1200
    )

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seed complete.")