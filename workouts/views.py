from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import WorkoutForm, ExerciseForm, SetForm
from .models import Workout, Exercise, WorkoutSet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def workout_list(request):

    workouts = Workout.objects.filter(user=request.user)

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

def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "workouts/register.html", {
        "form": form,
    })

def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("workout_list")

        else:
            return render(request, "workouts/login.html", {
                "error": "ユーザー名またはパスワードが正しくありません。",
            })

    return render(request, "workouts/login.html")

def logout_view(request):
    logout(request)

    return redirect("login")

@login_required
def set_create(request, exercise_id):

    exercise = get_object_or_404(
        Exercise,
        id=exercise_id,
        workout__user=request.user
    )

    if request.method == "POST":
        form = SetForm(request.POST)

        if form.is_valid():
            workout_set = form.save(commit=False)
            workout_set.exercise = exercise
            workout_set.save()

            return redirect("workout_list")

    else:
        form = SetForm()

    return render(request, "workouts/set_form.html", {
        "exercise": exercise,
        "form": form,
    })