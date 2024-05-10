from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


# Custom validator for allowing spaces in usernames
username_validator = RegexValidator(
    regex=r'^[\w .]*$',
    message="Username may only contain letters, numbers, underscores, periods, and spaces."
)

class User(AbstractUser):
    # Override the default username field
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],  # Apply the custom validator
        help_text='Required. 150 characters or fewer. Letters, numbers, underscores, periods, and spaces only.',
    )

    email = models.EmailField(unique=True, blank=False)  # Email field with unique constraint and blank=False
    is_evaluator = models.BooleanField(default=False)  # Default evaluator status to False

# Signal to create EvaluatorProfile when a new user is created
@receiver(post_save, sender=User)  # Register the signal
def create_evaluator_profile(sender, instance, created, **kwargs):
    from evaluation.models import EvaluatorProfile

    if created:
        # Create an empty EvaluatorProfile when a new user is created
        EvaluatorProfile.objects.create(user=instance)  # Ensure EvaluatorProfile is created for the new user



