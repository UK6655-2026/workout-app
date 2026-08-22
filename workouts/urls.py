from django.urls import path

from . import views


urlpatterns = [
    path("", views.workout_list, name="workout_list"),
]