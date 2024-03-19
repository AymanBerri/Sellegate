from django.contrib import admin
from .models import ShoppingCartItem, Transaction

# Register your models here.

admin.site.register(ShoppingCartItem)
admin.site.register(Transaction)