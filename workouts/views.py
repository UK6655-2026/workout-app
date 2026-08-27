from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import WorkoutForm, ExerciseForm, SetForm, GoalForm, WeightRecordForm
from .models import Workout, Exercise, WorkoutSet, Goal
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

def workout_delete(request, workout_id):

    workout = get_object_or_404(
        Workout,
        id=workout_id,
        user=request.user
    )

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return render(request, "workouts/workout_confirm_delete.html", {
        "workout": workout,
    })

def workout_edit(request, workout_id):

    workout = get_object_or_404(
        Workout,
        id=workout_id,
        user=request.user
    )

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)

        if form.is_valid():
            form.save()
            return redirect("workout_list")

    else:
        form = WorkoutForm(instance=workout)

    return render(request, "workouts/workout_form.html", {
        "form": form,
        "workout": workout,
    })

def exercise_delete(request, exercise_id):

    exercise = get_object_or_404(
        Exercise,
        id=exercise_id,
        workout__user=request.user
    )

    if request.method == "POST":
        exercise.delete()
        return redirect("workout_list")

    return render(request, "workouts/exercise_confirm_delete.html", {
        "exercise": exercise,
    })

def set_edit(request, set_id):

    workout_set = get_object_or_404(
        WorkoutSet,
        id=set_id,
        exercise__workout__user=request.user
    )

    if request.method == "POST":
        form = SetForm(request.POST, instance=workout_set)

        if form.is_valid():
            form.save()
            return redirect("workout_list")

    else:
        form = SetForm(instance=workout_set)

    return render(request, "workouts/set_form.html", {
        "form": form,
        "workout_set": workout_set,
    })

def set_delete(request, set_id):

    workout_set = get_object_or_404(
        WorkoutSet,
        id=set_id,
        exercise__workout__user=request.user
    )

    if request.method == "POST":
        workout_set.delete()
        return redirect("workout_list")

    return render(request, "workouts/set_confirm_delete.html", {
        "workout_set": workout_set,
    })

@login_required
def home(request):

    goal = Goal.objects.filter(
        user=request.user
    ).first()

    return render(request, "workouts/home.html", {
        "goal" : goal,
    })

@login_required
def weight_create(request):

    if request.method == "POST":

        form = WeightRecordForm(request.POST)

        if form.is_valid():

            weight_record = form.save(commit=False)
            weight_record.user = request.user
            weight_record.save()

            return redirect("home")

    else:

        form = WeightRecordForm()

    return render(request, "workouts/weight_form.html", {
        "form": form,
    })

@login_required
def goal_create(request):

    goal = Goal.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":

        form = GoalForm(
            request.POST,
            instance=goal
        )

        if form.is_valid():

            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()

            return redirect("home")

    else:

        form = GoalForm(
            instance=goal
        )

    return render(
        request,
        "workouts/goal_form.html",
        {
            "form": form,
            "goal": goal,
        }
    )