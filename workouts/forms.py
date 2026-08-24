from django import forms

from .models import Workout, Exercise, Set


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = [
            "workout_date",
            "memo",
        ]

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            "name",
        ]

class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = [
            "weight",
            "reps",
        ]