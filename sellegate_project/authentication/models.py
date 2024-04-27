from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)  # Email field with unique constraint and blank=False
    is_evaluator = models.BooleanField(default=False)


