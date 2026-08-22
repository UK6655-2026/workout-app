from django.shortcuts import redirect, render

from .forms import WorkoutForm
from .models import Workout

# Create your views here.
def workout_list(request):

    workouts = Workout.objects.all()

    if request.method == "POST":
        form = WorkoutForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("workout_list")
        else:
            print(form.errors)
    else:
        form = WorkoutForm()

    return render(request, "workouts/list.html", {
        "workouts": workouts,
        "form": form,
    })