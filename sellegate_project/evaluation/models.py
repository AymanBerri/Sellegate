# evaluation/models.py

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Evaluation(models.Model):
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('item_management.Item', on_delete=models.CASCADE)
    assessment = models.TextField()
    rating = models.IntegerField()
    # Other fields for evaluation details
