# item_management/serializers.py

from rest_framework import serializers
from .models import Item, Bid
from authentication.serializers import UserSerializer
from authentication.models import User

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item model.
    """

    # Use PrimaryKeyRelatedField for seller_id assuming seller is a ForeignKey to User model
    seller_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

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




class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'  # You can customize this based on your requirements
