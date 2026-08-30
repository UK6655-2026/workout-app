from django import forms

from .models import Workout, Exercise, WorkoutSet, Goal, WeightRecord


class WorkoutForm(forms.ModelForm):
    workout_date = forms.DateField(
        input_formats=[
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y.%m.%d",
        ]
    )

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
        model = WorkoutSet
        fields = [
            "weight",
            "reps",
        ]

class GoalForm(forms.ModelForm):

    class Meta:
        model = Goal

        fields = [
            "future_goal",
            "one_month_goal",
        ]

        labels = {
            "future_goal": "今後の目標",
            "one_month_goal": "1ヶ月後の目標",
        }

class WeightRecordForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=[
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y.%m.%d",
        ]
    )

    class Meta:
        model = WeightRecord
        fields = [
            "date",
            "weight",
        ]

        labels = {
            "date": "日付",
            "weight": "体重（kg）",
        }

