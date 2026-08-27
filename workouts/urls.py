from django.urls import path

from . import views


urlpatterns = [
    path("", views.workout_list, name="workout_list"),
    path("<int:workout_id>/exercise/add/",views.exercise_create,name="exercise_create",),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("<int:exercise_id>/set/add/",views.set_create,name="set_create"),
    path("<int:workout_id>/delete/",views.workout_delete,name="workout_delete"),
    path("<int:workout_id>/edit/",views.workout_edit,name="workout_edit"),
    path("exercise/<int:exercise_id>/delete/",views.exercise_delete,name="exercise_delete"),
    path("set/<int:set_id>/edit/",views.set_edit,name="set_edit"),
    path("set/<int:set_id>/delete/",views.set_delete,name="set_delete"),
    path("home/",views.home,name="home"),
    path("goal/",views.goal_create,name="goal_create"),
    path("weight/",views.weight_create,name="weight_create"),
]