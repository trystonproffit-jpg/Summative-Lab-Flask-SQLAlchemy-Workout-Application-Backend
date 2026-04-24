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

if __name__ == "__main__":
    app.run(port=5555, debug=True)