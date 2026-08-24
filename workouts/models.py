from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    future_goal = models.TextField()
    monthly_goal = models.TextField()

    def __str__(self):
        return self.future_goal


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_date = models.DateField()
    memo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_date}"


class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="exercises"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Set(models.Model):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="sets"
    )
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.weight}kg x {self.reps}回"


class WeightRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.weight}kg"