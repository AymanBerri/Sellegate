# item_management/serializers.py

from rest_framework import serializers
from .models import Item, Purchase, Bid
from authentication.serializers import UserSerializer
from authentication.models import User
from django.core.exceptions import ValidationError


# ItemResponseSerializer is what Frontend wants
# ItemSerializer is what i originally built

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for handling both creating and providing item data in the expected format.
    """
    # For response formatting
    seller_name = serializers.CharField(source='seller.username', read_only=True)  # Map seller's name
    created_at = serializers.SerializerMethodField()  # Custom method to format date
    evaluator_id = serializers.CharField(source='evaluation.evaluator.id', allow_null=True, read_only=True)
    
    # Optional thumbnail_url (defaulting to `null` if not provided)
    thumbnail_url = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'title',  # Name mapping
            'thumbnail_url',  # Optional image URL
            'description',
            'price',
            'seller_id',  # Original seller ID
            'seller_name',  # Human-readable seller name
            'created_at',
            'is_sold',
            'is_visible',
            'delegation_state',
            'evaluator_id',  # Can be null if not evaluated
        ]
        read_only_fields = ['id', 'seller_id', 'created_at', 'is_sold', 'seller_name']

    def get_created_at(self, obj):
        """
        Return the date in the required format (YYYY/MM/DD).
        """
        return obj.created_at.strftime("%Y/%m/%d")

    def create(self, validated_data):
        """
        Create a new item with validated data.
        """
        user = self.context['request'].user  # Current logged-in user
        validated_data['seller'] = user  # Set the seller to the logged-in user
        validated_data['is_sold'] = False  # Default value

        return Item.objects.create(**validated_data)



# class ItemResponseSerializer(serializers.ModelSerializer):
#     """
#     Serializer for providing item data in the expected format.
#     """
#     # Seller's name from the User model
#     seller_name = serializers.CharField(source='seller.username', read_only=True)  # Map seller's name
    
#     # Date formatting for created_at
#     created_at = serializers.SerializerMethodField()  # Custom method to format date
    
#     def get_created_at(self, obj):
#         return obj.created_at.strftime("%Y/%m/%d")  # Return the date in the required format

#     # Evaluator ID (nullable)
#     evaluator_id = serializers.CharField(source='evaluation.evaluator.id', allow_null=True, read_only=True)
    
#     class Meta:
#         model = Item
#         fields = [
#             'id',
#             'title',  # Assuming 'name' should map to 'title'
#             'thumbnail_url',
#             'description',
#             'price',
#             'seller_id',  # Original seller ID
#             'seller_name',  # Human-readable seller name
#             'created_at',
#             'is_sold',
#             'is_visible',
#             'delegation_state',
#             'evaluator_id',  # Can be null if not evaluated
#         ]

# class ItemCreateSerializer(serializers.ModelSerializer):
#     """
#     Serializer for creating a new item.
#     """
#     # The client might send an image, but default it to `null` for now
#     thumbnail_url = serializers.URLField(required=False, allow_null=True)  # Optional, defaulting to `null`

#     class Meta:
#         model = Item
#         fields = [
#             'title',  # Assumed mapping from 'name'
#             'description',
#             'price',
#             'thumbnail_url',  # Mapping from 'imgUrl'
#             'is_visible',  # User can choose
#             'delegation_state',  # Ensure it's one of the predefined choices
#         ]
    
#     def create(self, validated_data):
#         """
#         Create a new item with validated data.
#         """
#         user = self.context['request'].user  # Current logged-in user
#         validated_data['seller'] = user  # Set the seller as the current user
#         validated_data['is_sold'] = False  # Default value

#         # Return a new item instance
#         return Item.objects.create(**validated_data)




class ItemSerializer2(serializers.ModelSerializer):
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
