# item_management/serializers.py

from rest_framework import serializers
from .models import Item, Purchase, Bid
from authentication.serializers import UserSerializer
from authentication.models import User
from django.core.exceptions import ValidationError


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

    is_visible = serializers.BooleanField(required=True, allow_null=False)  # Explicitly required field
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'description',
            'price',
            'thumbnail_url',
            'seller_id',
            'delegation_state',
            'created_at',  
            'is_visible',  
            'is_sold', 
            
        ]
        read_only_fields = ['id', 'seller_id', 'created_at', 'is_sold']  # Fields that shouldn't be updated

    def validate(self, data):
        # List of read-only fields
        read_only_fields = ['seller_id', 'created_at', 'is_sold', 'id']

        # Check if any read-only field is being updated
        for field in read_only_fields:
            if field in data:
                raise serializers.ValidationError(f"Cannot update read-only field: {field}")

        return data  # Return validated data


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
    item_id = serializers.IntegerField(required=True)  # Ensure this field is required
    quantity = serializers.IntegerField(default=1)  # Default to 1 if not provided

    class Meta:
        model = Purchase
        fields = ['id', 'item_id', 'buyer_id', 'quantity', 'total_price', 'purchase_date']
        read_only_fields = ['id', 'purchase_date', 'total_price']  # Read-only derived fields

    def validate_item_id(self, value):
        """
        Validate that the item is valid, not sold, and visible.
        """
        if value <= 0:
            raise serializers.ValidationError("item_id must be a positive integer.")

        try:
            item = Item.objects.get(pk=value)
        except Item.DoesNotExist:
            raise serializers.ValidationError("Item not found.")

        if item.is_sold:
            raise serializers.ValidationError("This item has already been sold.")

        if not item.is_visible:
            raise serializers.ValidationError("This item is not visible and cannot be purchased.")

        return value

    def create(self, validated_data):
        """
        Create a new Purchase and calculate total_price.
        """
        item_id = validated_data['item_id']
        item = Item.objects.get(pk=item_id)

        # Default quantity to 1
        quantity = 1
        
        # Calculate total_price based on item price and quantity
        total_price = item.price * quantity
        print(validated_data)

        # Get the buyer instance from validated_data
        buyer = validated_data['buyer']

        # Create the Purchase
        return Purchase.objects.create(
            item=item,
            buyer=buyer,
            quantity=quantity,
            total_price=total_price,
        )

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'  # You can customize this based on your requirements
