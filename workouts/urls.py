from django.urls import path

from . import views


urlpatterns = [
    path("", views.workout_list, name="workout_list"),
    path("<int:workout_id>/exercise/add/",views.exercise_create,name="exercise_create",),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
    "<int:exercise_id>/set/add/",views.set_create,name="set_create"),
]