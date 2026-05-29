from marshmallow import Schema, fields, validate

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    
    # Schema Validation: Must be 0 or greater
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int(validate=validate.Range(min=0))

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    # Schema Validation: String length validation
    name = fields.Str(required=True, validate=validate.Length(min=2))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    # Schema Validation: Number range
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)

# Nested Schemas for stretch goals (combining entities)
class ExerciseWithWorkoutsSchema(ExerciseSchema):
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema))

class WorkoutWithExercisesSchema(WorkoutSchema):
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema))

# Schema Instantiations
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_with_workouts_schema = ExerciseWithWorkoutsSchema()
workout_with_exercises_schema = WorkoutWithExercisesSchema()
workout_exercise_schema = WorkoutExerciseSchema()