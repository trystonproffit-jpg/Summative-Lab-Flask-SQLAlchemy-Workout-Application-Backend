from flask import Flask, request
from flask_migrate import Migrate

from models import db, Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/")
def index():
    return {"message": "Workout API is running"}


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout_by_id(id):
    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404

    return workout_schema.dump(workout), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    try:
        validated_data = workout_schema.load(data)

        new_workout = Workout(**validated_data)

        db.session.add(new_workout)
        db.session.commit()

        return workout_schema.dump(new_workout), 201

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
    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return {"error": "Exercise not found"}, 404

    return exercise_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    try:
        validated_data = exercise_schema.load(data)

        new_exercise = Exercise(**validated_data)

        db.session.add(new_exercise)
        db.session.commit()

        return exercise_schema.dump(new_exercise), 201

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
        validated_data = workout_exercise_schema.load({
            **data,
            "workout_id": workout_id,
            "exercise_id": exercise_id
        })

        workout_exercise = WorkoutExercise(**validated_data)

        db.session.add(workout_exercise)
        db.session.commit()

        return workout_exercise_schema.dump(workout_exercise), 201

    except Exception as e:
        return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)