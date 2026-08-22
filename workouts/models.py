from django.db import models

# Create your models here.
class Workout(models.Model):
    exercise = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    workout_date = models.DateField()
    memo = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.exercise
    