from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import datetime

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema, workout_schema, workouts_schema,
    exercise_with_workouts_schema, workout_with_exercises_schema, workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Global error handler for Marshmallow Validations
@app.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400

# Global error handler for SQLAlchemy/Model Validations
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": str(e)}), 400

# --- WORKOUT ENDPOINTS ---

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify(workout_with_exercises_schema.dump(workout)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    data = workout_schema.load(json_data) 
    
    new_workout = Workout(
        date=data['date'], 
        duration_minutes=data['duration_minutes'], 
        notes=data.get('notes')
    )
    db.session.add(new_workout)
    db.session.commit()
    
    return jsonify(workout_schema.dump(new_workout)), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout and associated exercises deleted"}), 200


# --- EXERCISE ENDPOINTS ---

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return jsonify(exercise_with_workouts_schema.dump(exercise)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    data = exercise_schema.load(json_data)
    
    new_exercise = Exercise(
        name=data['name'],
        category=data['category'],
        equipment_needed=data.get('equipment_needed', False)
    )
    
    try:
        db.session.add(new_exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create exercise. Name must be unique."}), 400
        
    return jsonify(exercise_schema.dump(new_exercise)), 201

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200


# --- JOIN TABLE ENDPOINT ---

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    
    json_data = request.get_json()
    data = workout_exercise_schema.load(json_data) if json_data else {}
    
    new_we = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    
    db.session.add(new_we)
    db.session.commit()
    
    return jsonify(workout_exercise_schema.dump(new_we)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)