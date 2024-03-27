from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from item_management.models import Item

# Create your views here.

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_id = request.data.get('item_id')  # Assuming 'item_id' is sent in the request data
        quantity = request.data.get('quantity', 1)  # Default quantity is 1 if not provided

        # Retrieve the authenticated user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        try:
            item = Item.objects.get(id=item_id)  # Get the item based on the provided ID
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create or update the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        cart_item.quantity += int(quantity)
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Extract data from the request body
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)  # Default to 1 if quantity is not provided

        # Validate input data
        if not item_id:
            return Response({'error': 'Item ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        print("CREATED CART SUCCESS $$$$$$$$$$$$$$$$$$")
        # Add item to the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        print("ADDED ITEM SUCCESS $$$$$$$$$$$$$$$$$$")
        print(cart)

        # Serialize the cart and its items
        serializer = CartSerializer(cart)

        print("CART SERIALIZED SUCCESS $$$$$$$$$$$$$$$$$$")

        # Return the response
        return Response(serializer.data, status=status.HTTP_200_OK)


    # # If desired sending user_id instead of using the authenticated user
    # def post(self, request, format=None):
        user_id = request.data.get('userId')
        item_id = request.data.get('itemId')
        quantity = request.data.get('quantity')

        try:
            user_cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            user_cart = Cart.objects.create(user_id=user_id)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, item=item)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        user_cart_serializer = CartSerializer(user_cart)
        return Response(user_cart_serializer.data, status=status.HTTP_201_CREATED)