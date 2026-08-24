from django.urls import path

from . import views


urlpatterns = [
    path("", views.workout_list, name="workout_list"),
    path("<int:workout_id>/exercise/add/",views.exercise_create,name="exercise_create,"),
]