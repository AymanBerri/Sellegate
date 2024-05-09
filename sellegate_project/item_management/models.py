# item_management/models.py

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone  # Import timezone for automatic timestamp
# from authentication.models import User

User = get_user_model() # instead imported user model

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail_url = models.URLField(null=True, blank=True)  
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_items"  # Unique related_name for seller
    )
    evaluator = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="evaluator_items"  # Unique related_name for evaluator
    )

    # Define choices for delegation state
    DELEGATION_STATE_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Independent', 'Independent'), # User doesn't want to delegate
    )

    delegation_state = models.CharField(max_length=100, choices=DELEGATION_STATE_CHOICES)  # Add delegation state field with predefined choices
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for item creation
    is_visible = models.BooleanField(blank=False, null=False)  # Required, no default DOESNT WANT TO BE ENFORCED, JUST ENFORE IN FRONT-END
    is_sold = models.BooleanField(default=False)  # Indicates whether the item is sold

    def __str__(self):
        return self.title
    # Other fields for item details like condition, category, etc.

class Payment(models.Model):
    """
    Represents a record of a purchase or payment.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # The item being purchased
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)  # The buyer
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # The total price of the purchase
    created_at = models.DateTimeField(default=timezone.now)  # The timestamp of the purchase

    def __str__(self):
        return f"Payment for {self.item.title} by {self.buyer.username}"
    
    def save(self, *args, **kwargs):
        """
        Override the save method to set total_price to the related item's price.
        """
        if not self.total_price:  # If total_price is not set
            self.total_price = self.item.price  # Assign the price from the item
        super().save(*args, **kwargs)  # Call the parent save method





# OLD \/\/\/\/\/\/\/\/
class Purchase(models.Model):
    """
    Model to represent purchases made by users.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate `total_price` if not already set (THIS WAS ADDED TO HANDLE THE PROBLEM OF AHNDLING THE -
        # total_price WHEN CREATING A PURCHASE IN THE ADMIN WEBSITE)
        if self.total_price is None:
            self.total_price = self.item.price * self.quantity

        self.item.is_sold = True
        self.item.is_visible = False
        self.item.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase of {self.item.title} by {self.buyer.username}"
    def get_item_name(self):
        return self.item.title  # Return the title of the associated item


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields for bid details
