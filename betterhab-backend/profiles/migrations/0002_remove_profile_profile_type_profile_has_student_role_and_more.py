# Generated by Django 5.0.4 on 2024-05-10 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_type',
        ),
        migrations.AddField(
            model_name='profile',
            name='has_student_role',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='has_teacher_role',
            field=models.BooleanField(default=True),
        ),
    ]