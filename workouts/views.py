from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import WorkoutForm, ExerciseForm, SetForm, GoalForm, WeightRecordForm
from .models import Workout, Exercise, WorkoutSet, Goal, WeightRecord
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import calendar
from datetime import date


# Create your views here.
@login_required
def workout_list(request):

    workouts = Workout.objects.filter(user=request.user).order_by("-workout_date")

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
            return redirect("home")

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

    latest_weight = WeightRecord.objects.filter(
        user=request.user
    ).order_by("-date", "created_at").first()

    return render(request, "workouts/home.html", {
        "goal" : goal,
        "latest_weight": latest_weight,
    })

@login_required
def weight_create(request):

    if request.method == "POST":

        form = WeightRecordForm(request.POST)

        if form.is_valid():

            weight_record = form.save(commit=False)
            weight_record.user = request.user

            WeightRecord.objects.filter(
                user=request.user,
                date=weight_record.date
            ).delete()

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

@login_required
def weight_list(request):

    weights = WeightRecord.objects.filter(
        user=request.user
    ).order_by("date")

    return render(request, "workouts/weight_list.html", {
        "weights": weights,
    })

@login_required
def weight_edit(request, weight_id):

    weight = get_object_or_404(
        WeightRecord,
        id=weight_id,
        user=request.user
    )

    if request.method == "POST":

        form = WeightRecordForm(
            request.POST,
            instance=weight
        )

        if form.is_valid():

            form.save()

            return redirect("weight_list")

    else:

        form = WeightRecordForm(
            instance=weight
        )

    return render(request, "workouts/weight_form.html", {
        "form": form,
        "weight": weight,
    })

@login_required
def weight_delete(request, weight_id):

    weight = get_object_or_404(
        WeightRecord,
        id=weight_id,
        user=request.user
    )

    if request.method == "POST":

        weight.delete()

        return redirect("weight_list")

    return render(request, "workouts/weight_confirm_delete.html", {
        "weight": weight,
    })

@login_required
def workout_calendar(request):

    today = date.today()

    year_param = request.GET.get("year")
    month_param = request.GET.get("month")

    if year_param and month_param:
        year = int(year_param)
        month = int(month_param)
    else:
        year = today.year
        month = today.month

    # 前月
    if month == 1:
        previous_year = year - 1
        previous_month = 12
    else:
        previous_year = year
        previous_month = month - 1

    # 次月
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    cal = calendar.Calendar(firstweekday=6)

    month_days = cal.monthdayscalendar(year, month)

    workouts = Workout.objects.filter(
        user=request.user,
        workout_date__year=year,
        workout_date__month=month
    )

    workout_dates = {
        workout.workout_date.day
        for workout in workouts
    }

    return render(request, "workouts/calendar.html", {
        "year": year,
        "month": month,
        "month_days": month_days,
        "workout_dates": workout_dates,
        "previous_year": previous_year,
        "previous_month": previous_month,
        "next_year": next_year,
        "next_month": next_month,
    })

@login_required
def workout_day(request, year, month, day):

    workout = get_object_or_404(
        Workout,
        user=request.user,
        workout_date=date(year, month, day)
    )

    return render(request, "workouts/workout_day.html", {
        "workout": workout,
    })

@login_required
def statistics(request):

    workouts = Workout.objects.filter(
        user=request.user
    ).order_by("-workout_date")

    workout_count = workouts.count()

    exercise_count = Exercise.objects.filter(
        workout__user=request.user
    ).count()

    set_count = WorkoutSet.objects.filter(
        exercise__workout__user=request.user
    ).count()

    weights = WeightRecord.objects.filter(
        user=request.user
    ).order_by("date")

    exercises = Exercise.objects.filter(
        workout__user=request.user
    ).prefetch_related("sets", "workout")

    exercise_data = {}

    for exercise in exercises:

        if exercise.name not in exercise_data:
            exercise_data[exercise.name] = []

        for workout_set in exercise.sets.all():

            exercise_data[exercise.name].append({
                "date": exercise.workout.workout_date.strftime("%Y-%m-%d"),
                "weight": float(workout_set.weight),
            })

    for name in exercise_data:
        exercise_data[name].sort(
            key=lambda x: x["date"]
        )

    exercise_stats = []

    for name, records in exercise_data.items():

        max_weight = max(
            [record["weight"] for record in records],
            default=0
        )

        exercise_stats.append({
            "name": name,
            "max_weight": max_weight,
            "records": records,
        })

    return render(request, "workouts/statistics.html", {
        "workout_count": workout_count,
        "exercise_count": exercise_count,
        "set_count": set_count,
        "weights": weights,
        "exercise_stats": exercise_stats,
    })