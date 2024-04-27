# evaluation/models.py

from django.db import models
from django.contrib.auth import get_user_model
from item_management.models import Item

User = get_user_model()

class EvaluationRequest(models.Model):
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
