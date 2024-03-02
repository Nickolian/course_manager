from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    AUTHOR = 'author'
    STUDENT = 'student'
    USER_TYPE_CHOICES = [
        (AUTHOR, 'Автор'),
        (STUDENT, 'Студент'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=STUDENT)
