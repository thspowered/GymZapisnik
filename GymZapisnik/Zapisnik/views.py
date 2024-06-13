from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import WorkoutForm, ExerciseForm
from .models import Workout, Exercise, ExerciseCategory, Set, Tag


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'Neplatné přihlašovací údaje.')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})


def change_name(request):
    if request.method == 'POST':
        new_name = request.POST['new_name']
        request.user.username = new_name
        request.user.save()
        messages.success(request, 'Your name has been successfully changed.')
        return redirect('home')
    return render(request, 'ChangeName.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ChangePassword.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
    return render(request, 'logoutPage.html', {'username': username})
def create_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Workout created successfully.')
            return redirect('workoutAll')
    else:
        form = WorkoutForm()
    return render(request, 'createWorkout.html', {'form': form})

def my_workouts(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')

    return render(request, 'workoutAll.html', {'workouts': workouts})


def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)

    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        exercise = get_object_or_404(Exercise, pk=exercise_id)
        repetitions = request.POST.get('repetitions')
        weight = request.POST.get('weight')
        set = Set.objects.create(exercise=exercise, repetitions=repetitions, weight=weight)
        sets = exercise.sets.filter(workout=workout)
        messages.success(request, 'Set added successfully.')
        return redirect('workout_detail', workout_id=workout_id)

    return render(request, 'workout_detail.html', {'workout': workout})


def exercise_list(request, workout_id):
    exercises = Exercise.objects.all()
    categories = ExerciseCategory.objects.all()
    workout = get_object_or_404(Workout, pk=workout_id)

    show_favorites = request.GET.get('show_favorites') == 'true'

    favorite_tag, created = Tag.objects.get_or_create(name='Oblíbené', user=request.user)
    favorite_exercises = favorite_tag.exercises.all()


    if show_favorites:
        exercises = favorite_exercises
    else:
        exercises = Exercise.objects.all()

    category_ids = request.GET.getlist('categories')
    if category_ids:
        exercises = exercises.filter(category__in=category_ids)

    search_query = request.GET.get('search')
    if search_query:
        searched_exercises = Exercise.objects.filter(name__icontains=search_query)
        if show_favorites:
            exercises = searched_exercises.filter(pk__in=favorite_exercises.values_list('pk', flat=True))
        else:
            exercises = searched_exercises

    context = {'exercises': exercises, 'categories': categories, 'workout': workout}
    return render(request, 'exercise_list.html', context)
def add_exercise_to_workout(request, workout_id):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        workout = Workout.objects.get(pk=workout_id)
        exercise = Exercise.objects.get(pk=exercise_id)
        workout.exercises.add(exercise)
        return redirect('workout_detail', workout_id=workout_id)


def add_set_to_exercise(request, workout_id, exercise_id):
    if request.method == 'POST':
        workout = get_object_or_404(Workout, pk=workout_id)
        exercise = get_object_or_404(Exercise, pk=exercise_id)

        repetitions = request.POST.get('repetitions')
        weight = request.POST.get('weight')


        set = Set.objects.create(workout=workout, exercise=exercise, repetitions=repetitions, weight=weight,)


        return HttpResponseRedirect('/workout/{}/'.format(workout_id))
    else:
        return HttpResponse('Method not allowed')


def delete_exercise_from_workout(request, workout_id, exercise_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    exercise = get_object_or_404(Exercise, pk=exercise_id)

    workout.exercises.remove(exercise)

    Set.objects.filter(exercise=exercise).delete()

    return redirect('workout_detail', workout_id=workout_id)



def create_exercise(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    categories = ExerciseCategory.objects.all()
    form = ExerciseForm()
    if request.method == 'POST':
        name = request.POST.get('nazevCviku')
        description = request.POST.get('popisCviku')
        category_id = request.POST.get('kategorieCviku')
        category = ExerciseCategory.objects.get(id=category_id)
        new_exercise = Exercise.objects.create(name=name, description=description, category=category)
        return redirect('exercise_list', workout_id=workout_id)

    return render(request, 'CreateExercise.html', {'form': form, 'workout': workout, 'error_message': 'Neplatný formulář', 'categories': categories})


def add_to_favorite(request, workout_id, exercise_id):
    exercise = Exercise.objects.get(pk=exercise_id)
    workout = get_object_or_404(Workout, pk=workout_id)
    favorite_tag, created = Tag.objects.get_or_create(name='Oblíbené', user=request.user)

    if exercise in favorite_tag.exercises.all():
        favorite_tag.exercises.remove(exercise)
    else:
        favorite_tag.exercises.add(exercise)

    return redirect('exercise_list', workout_id=workout_id)


def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout updated successfully.')
            return redirect('workout_detail', workout_id=workout_id)
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'edit_workout.html', {'form': form, 'workout': workout})


def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, pk=workout_id)
    workout.delete()
    return redirect('workoutAll')

