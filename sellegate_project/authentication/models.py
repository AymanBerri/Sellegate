from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # Add a boolean field to distinguish evaluators from regular users
    is_evaluator = models.BooleanField(default=False)  # Flag to indicate whether the user is an evaluator or not
