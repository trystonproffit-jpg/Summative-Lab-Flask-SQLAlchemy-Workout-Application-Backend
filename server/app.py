from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Workout

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
    
    workouts_list = []

    for workout in workouts:
        workouts_list.append({
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes":workout.notes
        })

    return workouts_list, 200

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout_by_id(id):
    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404

    workout_dict = {
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": []
    }

    for workout_exercise in workout.workout_exercises:
        workout_dict["exercises"].append({
            "id": workout_exercise.exercise.id,
            "name": workout_exercise.exercise.name,
            "category": workout_exercise.exercise.category,
            "equipment_needed": workout_exercise.exercise.equipment_needed,
            "sets": workout_exercise.sets,
            "reps": workout_exercise.reps,
            "duration_seconds": workout_exercise.duration_seconds
        })

    return workout_dict, 200

if __name__ == "__main__":
    app.run(port=5555, debug=True)