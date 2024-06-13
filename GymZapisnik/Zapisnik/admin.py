from django.contrib import admin
from .models import Exercise, ExerciseCategory, Workout, Set, Tag

admin.site.register(Exercise)
admin.site.register(ExerciseCategory)
admin.site.register(Workout)
admin.site.register(Set)
admin.site.register(Tag)
