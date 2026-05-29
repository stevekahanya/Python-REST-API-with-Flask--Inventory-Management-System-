from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData, CheckConstraint

# Naming convention for migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    # Table Constraint 1: nullable=False & unique=True
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Relationship: An Exercise has many WorkoutExercises
    # cascade='all, delete-orphan' handles the stretch goal for deletion
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    # Model Validation 1: Ensure name is not empty or too short
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return name


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    # Table Constraint 2: CheckConstraint to enforce positive durations at the DB level
    duration_minutes = db.Column(db.Integer, CheckConstraint('duration_minutes > 0'), nullable=False)
    notes = db.Column(db.Text)

    # Relationship: A Workout has many WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    # Model Validation 2: Enforce duration logic at the application level
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if int(duration) <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return int(duration)


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    # Relationships back to parents
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')