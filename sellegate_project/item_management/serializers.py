# item_management/serializers.py

from rest_framework import serializers
from .models import Item, Bid

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  # You can customize this based on your requirements

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'  # You can customize this based on your requirements
