from django import forms
from .models import ExerciseCategory, Exercise, Workout, Set, Tag

class ExerciseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExerciseCategory
        fields = ['name']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'category']

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'date']


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['repetitions', 'weight']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'user', 'exercises']
