from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)  # Email field with unique constraint and blank=False
    is_evaluator = models.BooleanField(default=False)  # Default evaluator status to False


# Signal to create EvaluatorProfile when a new user is created
@receiver(post_save, sender=User)  # Register the signal
def create_evaluator_profile(sender, instance, created, **kwargs):
    from evaluation.models import EvaluatorProfile # DONT PUT THIS IN THE TOP OF THE FILE AS IT WILL CAUSE CIRCULAR IMPORT

    if created:
        # Create an empty EvaluatorProfile when a new user is created
        EvaluatorProfile.objects.create(user=instance)  # Ensure EvaluatorProfile is created for the new user
