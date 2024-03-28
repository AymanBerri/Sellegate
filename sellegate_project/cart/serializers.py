from rest_framework import serializers
from .models import Cart, CartItem
from item_management.serializers import ItemSerializer
from item_management.models import Item


class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()  # Define SerializerMethodField for subtotal
    # item_title = serializers.ReadOnlyField(source='item.title')  # Add item_title field to display item title

    class Meta:
        model = CartItem
        # fields = ['id', 'cart_id', 'item_id', 'item_title', 'quantity', 'created_at']
        fields = ['id', 'item_id', 'quantity', 'subtotal']
        read_only_fields = ['cart', 'created_at']  # These fields are read-only

    def get_subtotal(self, obj):
        """
        Method to get the subtotal for the cart item from the model's subtotal method.
        """
        return obj.subtotal()  # Call the model's subtotal method

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Serializer for cart items

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'items']
        read_only_fields = ['user', 'created_at', 'items']  # These fields are read-only

    









# OLD
# class CartItemSerializer(serializers.ModelSerializer):
#     item_id = serializers.PrimaryKeyRelatedField(source='item', queryset=Item.objects.all())
#     quantity = serializers.IntegerField(min_value=1)

#     class Meta:
#         model = CartItem
#         fields = ['item_id', 'quantity']



# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)  # Serialize the associated cart items

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'items']  # You may include additional fields if needed