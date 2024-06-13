# Generated by Django 5.0.6 on 2024-05-13 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zapisnik', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='exercises',
            field=models.ManyToManyField(related_name='workouts', to='Zapisnik.exercise'),
        ),
        migrations.AddField(
            model_name='workout',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]