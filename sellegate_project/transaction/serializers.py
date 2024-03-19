# transaction/serializers.py

from rest_framework import serializers
from .models import Transaction, ShoppingCartItem

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # You can customize this based on your requirements

class ShoppingCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = '__all__'  # You can customize this based on your requirements
