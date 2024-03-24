# item_management/models.py

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail_url = models.URLField(null=True, blank=True)  
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    # Other fields for item details like condition, category, etc.

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields for bid details
