# evaluation/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from item_management.models import Item
# from authentication.models import User

User = get_user_model() #this will cause a problem because of User import


class EvaluationRequest(models.Model):
    """
    Represents a request to assess or evaluate an item.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Item to be assessed
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)  # User making the assessment request
    name = models.CharField(max_length=255)  # Title of the assessment
    message = models.TextField()  # Assessment message
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Estimated price
    state = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp of the request

    def __str__(self):
        return f"Assessment Request: {self.name} by {self.evaluator.username}"


class EvaluatorProfile(models.Model):
    """
    Model to represent the evaluator profile. One-to-one with User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensure the profile is deleted if the user is deleted
    bio = models.TextField(default="", blank=True)  # Default bio to empty string
    
# OLD \/\/\/\/\/\/\/\/\
class OLDEvaluationRequest(models.Model):
    # Define status choices for the evaluation request
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
 
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='requested'  # Default to 'requested' when a new request is created
    )
    request_date = models.DateTimeField(auto_now_add=True)


