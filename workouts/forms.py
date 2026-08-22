from django import forms

from .models import Workout


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout

        fields = [
            "exercise",
            "weight",
            "reps",
            "sets",
            "workout_date",
            "memo",
        ]