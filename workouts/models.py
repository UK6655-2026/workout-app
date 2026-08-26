from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="workouts"
    )
    workout_date = models.DateField()
    memo = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.workout_date)


class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="exercises"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkoutSet(models.Model):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="sets"
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    reps = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.weight}kg × {self.reps}回"

