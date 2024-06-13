from django.urls import path
from .views import (login_view, home_view, change_password, change_name,
                    logout_view, register_view, create_workout, my_workouts, workout_detail,
                    exercise_list, add_exercise_to_workout, add_set_to_exercise, delete_exercise_from_workout,
                    create_exercise, add_to_favorite, edit_workout, delete_workout, )

urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('change_password/', change_password, name='change_password'),
    path('change_name/', change_name, name='change_name'),
    path('logout/', logout_view, name='logout'),
    path('create_workout/', create_workout, name='create_workout'),
    path('my_workouts/', my_workouts, name='workoutAll'),
    path('workout/<int:workout_id>/', workout_detail, name='workout_detail'),
    path('exercise_list/<int:workout_id>/', exercise_list, name='exercise_list'),
    path('add_exercise_to_workout/<int:workout_id>/', add_exercise_to_workout, name='add_exercise_to_workout'),
    path('workout/<int:workout_id>/add_set/<int:exercise_id>/', add_set_to_exercise, name='add_set_to_exercise'),
    path('workout/<int:workout_id>/delete_exercise/<int:exercise_id>/', delete_exercise_from_workout, name='delete_exercise_from_workout'),
    path('create_exercise/<int:workout_id>', create_exercise, name='create_exercise'),
    path('add_to_favorite/<int:workout_id>/<int:exercise_id>/', add_to_favorite, name='add_to_favorite'),
    path('workout/<int:workout_id>/edit/', edit_workout, name='edit_workout'),
    path('delete_workout/<int:workout_id>/', delete_workout, name='delete_workout'),

]
