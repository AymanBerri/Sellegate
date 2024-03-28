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
        item_id = request.data.get('item_id')  
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

        # Serialize the entire cart including its items
        cart_serializer = CartSerializer(cart)

        if created:
            message = "Item added to the cart successfully"
            status_code = status.HTTP_201_CREATED
        else:
            message = "Item quantity updated in the cart successfully"
            status_code = status.HTTP_200_OK

        return Response({"message": message, "data": cart_serializer.data}, status=status_code)

# class AddToCartAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         item_id = request.data.get('item_id')  
#         quantity = request.data.get('quantity', 1)  # Default quantity is 1 if not provided

#         # Retrieve the authenticated user's cart
#         cart, created = Cart.objects.get_or_create(user=request.user)

#         try:
#             item = Item.objects.get(id=item_id)  # Get the item based on the provided ID
#         except Item.DoesNotExist:
#             return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Create or update the cart item
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
#         cart_item.quantity += int(quantity)
#         cart_item.save()

#         # Serialize the entire cart including its items
#         cart_serializer = CartSerializer(cart)

#         return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
    

class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get item_id and quantity from request data
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        # Check if item_id is provided
        if not item_id:
            return Response({"error": "item_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the cart item
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, item_id=item_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in the user's cart"}, status=status.HTTP_404_NOT_FOUND)

        # If quantity is not provided, remove the entire cart item
        if quantity is None:
            cart_item.delete()
            message = "Item removed from the cart successfully"
        else:
            # Lower the quantity of the cart item
            if int(quantity) >= cart_item.quantity:
                cart_item.delete()
                message = "Item removed from the cart successfully"
            else:
                cart_item.quantity -= int(quantity)
                cart_item.save()
                message = "Item quantity lowered in the cart successfully"

        # Serialize the entire cart including its items
        cart = cart_item.cart
        cart_serializer = CartSerializer(cart)

        # Return response with serialized data and message
        return Response({"message": message, "data": cart_serializer.data}, status=status.HTTP_200_OK)