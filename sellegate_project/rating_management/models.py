from django.db import models

# Create your models here.

class EvaluatorRating(models.Model):
    evaluator_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField()
    user_id = models.IntegerField()

class SellerRating(models.Model):
    seller_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField()
    user_id = models.IntegerField()
