from django.db import models
from django.contrib.auth.models import User

class ExerciseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def sets(self):
        return Set.objects.filter(exercise=self)

class Workout(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    exercises = models.ManyToManyField('Exercise', related_name='workouts')

    def __str__(self):
        return f"Workout on {self.date}"

class Set(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.IntegerField()
    weight = models.FloatField()


    unique_together = ('workout', 'exercise')

    def __str__(self):
        return f"Set {self.id} - {self.exercise.name} in Workout {self.workout.id}"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise)

    objects = models.Manager()

    def __str__(self):
        return self.name
