from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_teacher_role = models.BooleanField(default=True)
    has_student_role = models.BooleanField(default=True)

    # Additional fields like biography can be added here later

    def __str__(self):
        return f'{self.user.username} Profile'
