# transaction/models.py

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('item_management.Item', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields for transaction details like payment status, order status, etc.

class ShoppingCartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('item_management.Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    # Other fields for shopping cart item details
