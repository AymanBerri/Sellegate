from django.db import models
from authentication.models import User
from item_management.models import Item
from django.utils import timezone


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 0)
    created_at = models.DateTimeField(default=timezone.now)

    def subtotal(self):
        return self.quantity * self.item.price
    
    def __str__(self):
        return self.item.title  # Display item title in the admin interface




# OLD
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Item, through='CartItem')

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)