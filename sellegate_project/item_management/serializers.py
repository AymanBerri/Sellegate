# item_management/serializers.py

from rest_framework import serializers
from .models import Item, Purchase, Bid
from authentication.serializers import UserSerializer
from authentication.models import User

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item model.
    """

    # Use PrimaryKeyRelatedField for seller_id assuming seller is a ForeignKey to User model
    # Establishes a relationship to a User model by its primary key
    seller_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # This field ensures that only valid user IDs are accepted during validation.
    # If the provided ID does not correspond to an existing user, it raises an "Invalid pk" exception.
    # Django REST Framework automatically checks whether the referenced user exists in the database.

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'price', 'thumbnail_url', 'seller_id', 'delegation_state']

    def create(self, validated_data):
        """
        Create a new item instance.

        :param validated_data: Validated data for creating the item
        :return: Newly created item instance
        """

        # Extract seller from validated data
        seller = validated_data.pop('seller_id')
        
        # Create and return the new item instance
        item = Item.objects.create(seller=seller, **validated_data)
        return item

class PurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Purchase model.
    """

    class Meta:
        model = Purchase
        fields = ['id', 'item_id', 'buyer_id', 'quantity', 'total_price', 'purchase_date']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'  # You can customize this based on your requirements
