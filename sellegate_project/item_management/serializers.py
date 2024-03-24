# item_management/serializers.py

from rest_framework import serializers
from .models import Item, Bid
from authentication.serializers import UserSerializer

class ItemSerializer(serializers.ModelSerializer):
    seller = UserSerializer()  # Nested serializer for the seller

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'price', 'thumbnail_url', 'seller']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'  # You can customize this based on your requirements
