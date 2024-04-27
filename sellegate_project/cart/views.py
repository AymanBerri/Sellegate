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
    """
AddToCartAPIView:
-----------------
This API view is responsible for adding an item to the user's cart. 
"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
            ### Adding an Item to the Cart with Postman (Form Data)

            To add an item to the cart in Postman, follow these steps:

            1. **Set the HTTP Method to POST**:
            - Select `POST` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Use the URL for adding an item to the cart. Example: `http://localhost:8000/api/cart/`.

            3. **Set the Headers**:
            - Add the `Authorization` header with your token:
                - `Authorization`: `Token <your_token_here>`  # Replace with your token
            - `Content-Type` will be set automatically for form data.

            4. **Set the Request Body**:
            - Click on the "Body" tab.
            - Choose `form-data`.
            - Add the key-value pairs to add an item to the cart:
                - `item_id`: `1`  # Replace with the desired item ID
                - `quantity`: `1`  # Optional, defaults to 1 if not provided

            5. **Send the Request**:
            - Click "Send" to submit the request.
            - If successful, you should get a 201 Created or 200 OK response with the updated cart data.
            - If there's an error, check the response for details.

            6. **Common Error Responses**:
            - **400 Bad Request**: If `item_id` or `quantity` cannot be converted to an integer, or if the item's delegation state is not "Independent" or "Approved".
            - **404 Not Found**: If the specified item does not exist.
            """


        try:
            item_id = int(request.data.get('item_id'))
        except (TypeError, ValueError):
            return Response({"error": "Invalid item_id. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = int(request.data.get('quantity', 1))  # Default quantity to 1
        except (TypeError, ValueError):
            return Response({"error": "Invalid quantity. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the authenticated user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        try:
            item = Item.objects.get(id=item_id)  # Get the item based on the provided ID
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the item's delegation_state allows adding to the cart 
        if item.delegation_state not in ["Independent", "Approved"]:
            return Response({"error": f"Item cannot be added to the cart due to its delegation state - {item.delegation_state}."}, status=status.HTTP_400_BAD_REQUEST)

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


class RemoveFromCartAPIView(APIView):
    """
    RemoveFromCartAPIView:
    ----------------------
    This API view is responsible for removing an item from the user's cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        ### Removing an Item from the Cart with Postman (Form Data)

        To remove an item from the cart in Postman, follow these steps:

        1. **Set the HTTP Method to POST**:
        - Select `POST` from the method dropdown.

        2. **Enter the Endpoint URL**:
        - Use the endpoint for removing an item from the cart. Example: `http://localhost:8000/api/cart/remove/`.

        3. **Set the Headers**:
        - Add the `Authorization` header with your token:
            - `Authorization`: `Token <your_token_here>`  # Replace with your actual token
        - `Content-Type` will be set automatically for form data.

        4. **Set the Request Body**:
        - Click on the "Body" tab.
        - Choose `form-data`.
        - Add the following key-value pairs to remove an item from the cart:
            - `item_id`: `1`  # ID of the item to remove
            - `quantity`: `1`  # Optional, defaults to 1. If not provided, removes the entire item.

        5. **Send the Request**:
        - Click "Send" to submit the request.
        - If successful, you should get a 200 OK response with the updated cart data and a success message.
        - If the request fails, check the response for error details.

        6. **Common Error Responses**:
        - **400 Bad Request**: If `item_id` or `quantity` cannot be converted to an integer, or if `item_id` is not provided.
        - **404 Not Found**: If the item doesn't exist in the user's cart.
        """


        # Get item_id and quantity from request data
        try:
            item_id = int(request.data.get('item_id'))
        except (TypeError, ValueError):
            return Response({"error": "Invalid item_id. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = int(request.data.get('quantity', 1))  # Default quantity to 1
        except (TypeError, ValueError):
            return Response({"error": "Invalid quantity. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

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