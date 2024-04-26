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


    # Define choices for delegation state
    DELEGATION_STATE_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Independent', 'Independent'), # User doesn't want to delegate
    )

    delegation_state = models.CharField(max_length=100, choices=DELEGATION_STATE_CHOICES)  # Add delegation state field with predefined choices

    # Other fields for item details like condition, category, etc.

class Purchase(models.Model):
    """
    Model to represent purchases made by users.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Purchase of {self.item.title} by {self.buyer.username}"
    def get_item_name(self):
        return self.item.title  # Return the title of the associated item


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields for bid details
