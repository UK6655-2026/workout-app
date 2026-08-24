from django.shortcuts import redirect, render, get_object_or_404

from .forms import WorkoutForm, ExerciseForm, SetForm
from .models import Workout, Exercise


# Create your views here.
def workout_list(request):

    workouts = Workout.objects.all()

    if request.method == "POST":
        workout_form = WorkoutForm(request.POST)

        if workout_form.is_valid():
            workout = workout_form.save(commit=False)
            workout.user = request.user
            workout.save()

            return redirect("workout_list")
    else:
        workout_form = WorkoutForm()

    return render(request, "workouts/list.html", {
        "workouts": workouts,
        "workout_form": workout_form,
    })


def exercise_create(request, workout_id):

    workout = get_object_or_404(Workout, id=workout_id)

    if request.method == "POST":
        form = ExerciseForm(request.POST)

        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout = workout
            exercise.save()

            return redirect("workout_list")

    else:
        form = ExerciseForm()

    return render(request, "workouts/exercise_form.html", {
        "workout": workout,
        "form": form,
    })