from flask import Flask, request
from flask_migrate import Migrate
from datetime import datetime

from models import db, Workout, Exercise, WorkoutExercise

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    return {"message": "Workout API is running"}


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return [{
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes
    } for workout in workouts], 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout_by_id(id):
    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404

    return {
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": [{
            "id": workout_exercise.exercise.id,
            "name": workout_exercise.exercise.name,
            "category": workout_exercise.exercise.category,
            "equipment_needed": workout_exercise.exercise.equipment_needed,
            "sets": workout_exercise.sets,
            "reps": workout_exercise.reps,
            "duration_seconds": workout_exercise.duration_seconds
        } for workout_exercise in workout.workout_exercises]
    }, 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    try:
        new_workout = Workout(
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes")
        )

        db.session.add(new_workout)
        db.session.commit()

        return {
            "id": new_workout.id,
            "date": new_workout.date.isoformat(),
            "duration_minutes": new_workout.duration_minutes,
            "notes": new_workout.notes
        }, 201

    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)
    db.session.commit()

    return {}, 204


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return [{
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed
    } for exercise in exercises], 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return {"error": "Exercise not found"}, 404

    return {
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": [{
            "id": workout_exercise.workout.id,
            "date": workout_exercise.workout.date.isoformat(),
            "duration_minutes": workout_exercise.workout.duration_minutes,
            "notes": workout_exercise.workout.notes,
            "sets": workout_exercise.sets,
            "reps": workout_exercise.reps,
            "duration_seconds": workout_exercise.duration_seconds
        } for workout_exercise in exercise.workout_exercises]
    }, 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    try:
        new_exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data.get("equipment_needed", False)
        )

        db.session.add(new_exercise)
        db.session.commit()

        return {
            "id": new_exercise.id,
            "name": new_exercise.name,
            "category": new_exercise.category,
            "equipment_needed": new_exercise.equipment_needed
        }, 201

    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)
    db.session.commit()

    return {}, 204


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        return {"error": "Workout not found"}, 404

    if not exercise:
        return {"error": "Exercise not found"}, 404

    data = request.get_json()

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return {
            "id": workout_exercise.id,
            "workout_id": workout_exercise.workout_id,
            "exercise_id": workout_exercise.exercise_id,
            "reps": workout_exercise.reps,
            "sets": workout_exercise.sets,
            "duration_seconds": workout_exercise.duration_seconds
        }, 201

    except Exception as e:
        return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)