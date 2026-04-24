from marshmallow import Schema, fields, validates, validates_schema, ValidationError


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be greater than 0.")

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be greater than 0.")

    @validates("duration_seconds")
    def validate_duration_seconds(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration seconds must be greater than 0.")

    @validates_schema
    def validate_reps_sets_or_duration(self, data, **kwargs):
        has_reps_sets = data.get("reps") is not None and data.get("sets") is not None
        has_duration = data.get("duration_seconds") is not None

        if not has_reps_sets and not has_duration:
            raise ValidationError("Provide either reps and sets, or duration_seconds.")


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(missing=False)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

    @validates("name")
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise ValidationError("Exercise name must be at least 2 characters.")

    @validates("category")
    def validate_category(self, value):
        allowed = ["Strength", "Cardio", "Flexibility", "Balance"]
        if value not in allowed:
            raise ValidationError(f"Category must be one of: {', '.join(allowed)}.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

    @validates("duration_minutes")
    def validate_duration_minutes(self, value):
        if value <= 0:
            raise ValidationError("Duration must be greater than 0.")