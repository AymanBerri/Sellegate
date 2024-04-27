from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Item, Purchase
from .serializers import ItemSerializer, PurchaseSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from django.core.exceptions import PermissionDenied



class PurchaseItemAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    
    def post(self, request, format=None):
        """
            ### Creating a Purchase with Postman

            To create a new purchase using Postman, follow these steps:

            1. **Set HTTP Method to POST**:
            - Select `POST` from the method dropdown menu.

            2. **Enter the Endpoint URL**:
            - Use the URL for creating a purchase. Example: `http://localhost:8000/items/buy/`.

            3. **Set the Headers**:
            - Add the `Authorization` header with your authentication token:
                - `Authorization`: `Token <your_token>`  # Replace `<your_token>` with your actual token

            4. **Set the Request Body**:
            - Click on the "Body" tab.
            - Choose `form-data`.
            - Add the following key-value pairs to create a purchase:
                - `item_id`: `1`  # ID of the item to be purchased

            5. **Send the Request**:
            - Click "Send" to submit the POST request.
            - If successful, you should receive a `201 Created` response with the purchase details.
            - If there's an error, check the response for validation errors or other issues.

            ### Common Error Responses

            - **400 Bad Request**: If the request data is invalid (e.g., missing required fields, incorrect data type, etc.).
            - **404 Not Found**: If the specified `item_id` does not exist.
        """
       
        # Validate the request data with the serializer
        serializer = PurchaseSerializer(data=request.data)

        if not serializer.is_valid():
            # Return the validation errors with a 400 status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the authenticated user
        buyer = request.user

        # If validation passes, create the Purchase with the correct buyer
        purchase = serializer.save(buyer=buyer)  # Pass the User instance

        # Additional business logic: update item status
        item = Item.objects.get(pk=purchase.item.id)
        item.is_sold = True
        item.is_visible = False
        item.save()

        # Return the response with the serialized Purchase data
        return Response(PurchaseSerializer(purchase).data, status=status.HTTP_201_CREATED)

class ItemListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication to create an item

    def post(self, request, format=None):
        """
        ### Creating an Item with Postman

        To create a new item in Postman, use the following steps:

        1. **Set the HTTP Method to POST**:
        - Select `POST` from the method dropdown.

        2. **Enter the Endpoint URL**:
        - Use the correct endpoint for creating an item. Example: `http://localhost:8000/items/`.

        3. **Set the Headers**:
        - Add the `Authorization` header with your authentication token:
            - `Authorization`: `Token <your_token>`  # Replace `<your_token>` with your actual token
        - If using form data, Postman will automatically set the `Content-Type`.

        4. **Set the Request Body**:
        - Click on the "Body" tab.
        - Choose `form-data`.
        - Add the key-value pairs to create a new item. Ensure all required fields are provided:
            - `title`: `"Item Title"`  # Required
            - `description`: `"Item Description"`  # Required
            - `price`: `"99.99"`  # Required (Use appropriate price format)
            - `delegation_state`: `"Pending"`  # Required (Choose from the defined states)
            - `is_visible`: `"true"`  # Required, must be explicitly set to `true` or `false`
        - Optional fields, if needed:
            - `thumbnail_url`: `"http://example.com/image.jpg"`  # Optional thumbnail image URL

        5. **Send the Request**:
        - Click "Send" to submit the POST request.
        - If successful, you'll receive a `201 Created` response with the serialized item data.
        - If there's an error, check the response body for validation errors or other issues.

        6. **Handling Errors**:
        - If you get a `400 Bad Request` response, examine the response body to understand which fields are missing or invalid.
        - Ensure that all required fields are included in the request body and are properly formatted.
        - Ensure that `is_visible` is explicitly set to avoid defaulting or null values.

        7. **Seller ID Handling**:
        - The `seller_id` is set automatically based on the authenticated user. It is not required in the request payload.

        ### Notes on `is_visible`:
        - To avoid unexpected behavior or default values, ensure that `is_visible` is explicitly set in the front-end to either `true` or `false`.
        - If `is_visible` is missing or has an invalid value, the request will result in a `400 Bad Request` error.
        """

        # Ensure the seller is the authenticated user
        data = request.data.copy()  # Create a copy of the request data
        data['seller_id'] = request.user.id  # Set seller_id to the authenticated user ID

        # Create a serializer instance with the updated data
        serializer = ItemSerializer(data=data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # If valid, save the item to the database
            item = serializer.save()
            # Return the serialized data with status 201 (Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If serializer is not valid, return errors with status 400 (Bad Request)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemSearchAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]  # Allow public access, no token required


    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]  # Add filter backends for search and ordering

    search_fields = ['title', 'description', 'seller__username']  # Specify fields for search
    ordering_fields = ['price']  # Specify fields for ordering

    def get_queryset(self):
        """
            ### Searching Items with Postman

            To send a GET request to search for items in Postman:

            1. **Set the HTTP Method to GET**:
            - Select `GET` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Use the URL for the item search endpoint, like `http://localhost:8000/items/search/`.

            3. **Set the Query Parameters**:
            - Click on the "Params" tab.
            - Add key-value pairs for the filters. Examples:
                - `query`: `"search_term"`  # Search by title or description
                - `category`: `"desired_category"`  # Filter by category (Not implemented yet)
                - `minPrice`: `"minimum_price"`  # Filter by minimum price
                - `maxPrice`: `"maximum_price"`  # Filter by maximum price

            4. **Send the Request**:
            - Click "Send" to submit the request.
            - If successful, you'll receive a JSON response with the filtered items.
            - You can use the "Search Fields" to filter by title or description, and "Ordering Fields" to order by price.

            5. **Handle Response**:
            - If successful, examine the returned JSON data to understand the structure of the response.
            - If the request fails, check the error message for details on what might have gone wrong.
            """

        queryset = super().get_queryset()  # Get the queryset from the parent class

        # Apply filters based on query parameters:

        # Filter by search query
        query = self.request.query_params.get('query')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Filter by minimum price
        min_price = self.request.query_params.get('minPrice')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        # Filter by maximum price
        max_price = self.request.query_params.get('maxPrice')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset  # Return the filtered queryset

class ItemDetailView(APIView):
    def get(self, request, item_id, format=None):
        """
            ### Retrieving Item Details with Postman

            To send a GET request to retrieve item details in Postman, follow these steps:

            1. **Set the HTTP Method to GET**:
            - Select `GET` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Use the URL for the item detail endpoint, including the item ID. Example: `http://localhost:8000/items/1/` (where `1` is the item ID).

            3. **Set the Headers**:
            - If authentication is required, add the `Authorization` header with your token:
                - `Authorization`: `Token <your_token_here>`  # Replace with your token

            4. **Send the Request**:
            - Click "Send" to retrieve the item details.
            - If successful, you should get a 200 OK response with the serialized item data.
            - If the item doesn't exist, you'll receive a 404 Not Found error.

            5. **Common Error Responses**:
            - **404 Not Found**: If the item ID doesn't match any item in the database, this error is returned.
            """

        try:
            item = Item.objects.get(pk=item_id)  # Retrieve the item by its ID
            serializer = ItemSerializer(item)  # Serialize the item
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return the serialized data
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)  # Return 404 if item is not found
        
class UserPurchasesAPIView(APIView):
    """
    API endpoint to get all purchases of the authenticated user.
    """
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, format=None):

        """
            ### Fetching All Purchases of the Authenticated User with Postman

            To fetch all purchases made by the authenticated user, follow these steps:

            1. **Set HTTP Method to GET**:
            - Select `GET` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Use the URL for fetching purchases. Example: `http://localhost:8000/items/my-purchases/`.

            3. **Set the Headers**:
            - Add the `Authorization` header with your authentication token:
                - `Authorization`: `Token <your_token_here>`  # Replace `<your_token_here>` with your actual token

            4. **Send the Request**:
            - Click "Send" to submit the GET request.
            - If successful, you'll receive a `200 OK` response with the serialized list of purchases.

            5. **Handling Errors**:
            - If the response is empty, it may indicate no purchases were found for the authenticated user.
            - If you receive a `401 Unauthorized`, ensure your authentication token is valid and you have appropriate permissions.
            """

        # Get all purchases for the authenticated user
        purchases = Purchase.objects.filter(buyer=request.user)

        if purchases.exists():  # Check if there are any purchases
            # Serialize the purchases
            serializer = PurchaseSerializer(purchases, many=True)

            # Return the serialized data with HTTP 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no purchases were found, return a message indicating that
            return Response(
                {"message": "No purchases found for this user."},
                status=status.HTTP_200_OK
            )

class UserSoldItemsAPIView(APIView):
    """
    API endpoint to get all items sold by the authenticated user.
    """
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, format=None):
        """
        ### Fetching All Sold Items of the Authenticated User with Postman

        To fetch all items sold by the authenticated user, follow these steps:

        1. **Set HTTP Method to GET**:
        - Select `GET` from the method dropdown.

        2. **Enter the Endpoint URL**:
        - Use the URL for fetching sold items. Example: `http://localhost:8000/items/my-sold-items/`.

        3. **Set the Headers**:
        - Add the `Authorization` header with your authentication token:
            - `Authorization`: `Token <your_token_here>`  # Replace `<your_token_here>` with your actual token

        4. **Send the Request**:
        - Click "Send" to submit the GET request.
        - If successful, you'll receive a `200 OK` response with the serialized list of sold items.

        5. **Handling Errors**:
        - If the response is empty, it may indicate no items were sold by the authenticated user.
        - If you receive a `401 Unauthorized`, ensure your authentication token is valid and you have appropriate permissions.

        ### Important Note
        This endpoint returns only the items that have been sold (`is_sold = true`). It does not return all items listed by the user.
        """

        # Get all items where the authenticated user is the seller
        items_sold = Item.objects.filter(seller=request.user, is_sold=True)

        if items_sold.exists():  # Check if there are any sold items
            # Serialize the items
            serializer = ItemSerializer(items_sold, many=True)

            # Return the serialized data with HTTP 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no sold items were found, return a message indicating that
            return Response(
                {"message": "No items sold by this user."},
                status=status.HTTP_200_OK
            )
        
class UpdateItemAPIView(APIView):
    """
    API endpoint to update an item by ID.
    The user must be authenticated and the owner/seller of the item.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id, format=None):
        ALLOWED_FIELDS = ["title", "description", "price", "thumbnail_url", "delegation_state", "is_visible"]

        if not request.data:
            # If the request body is empty, return feedback
            return Response(
                {"error": "No fields provided for update."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the item by ID
            item = Item.objects.get(id=item_id)

            # Ensure the authenticated user is the seller/owner of the item
            if item.seller != request.user:
                raise PermissionDenied("You do not have permission to update this item.")

            # Check for any fields that are not allowed for update
            invalid_fields = [field for field in request.data.keys() if field not in ALLOWED_FIELDS]

            if invalid_fields:
                # Return an error message if there are invalid fields
                return Response(
                    {"error": f"Cannot update the following fields: {', '.join(invalid_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Use the serializer for partial updates
            serializer = ItemSerializer(item, data=request.data, partial=True)

            if serializer.is_valid():
                # Save the valid data
                item_updated = serializer.save()

                # Return success response with updated item data
                return Response(
                    {"message": "Item updated successfully.", "item": ItemSerializer(item_updated).data},
                    status=status.HTTP_200_OK
                )
            else:
                # If validation fails, return errors with a 400 status
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Item.DoesNotExist:
            # Return a 404 if the item does not exist
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied:
            # Return a 403 if the user does not have permission
            return Response({"error": "You do not have permission to update this item."}, status=status.HTTP_403_FORBIDDEN)

class DeleteItemAPIView(APIView):
    """
    API endpoint to delete an item by ID.
    The user must be authenticated and be the owner or seller of the item.
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, item_id, format=None):
        """
        ### Deleting an Item with Postman

        To delete an item using Postman, follow these steps:

        1. **Set HTTP Method to DELETE**:
        - Select `DELETE` from the method dropdown.

        2. **Enter the Endpoint URL**:
        - Use the URL for deleting an item by its ID. Example: `http://localhost:8000/items/delete-item/1/`.

        3. **Set the Headers**:
        - Add the `Authorization` header with your authentication token:
            - `Authorization`: `Token <your_token_here>`  # Replace `<your_token_here>` with your actual token

        4. **Send the Request**:
        - Click "Send" to submit the DELETE request.
        - If successful, you'll receive a `200 OK` response with a success message.
        - If there's an error, check the response body for details.

        5. **Handling Errors**:
        - **404 Not Found**: If the item ID does not exist.
        - **403 Forbidden**: If you don't have permission to delete the item (you are not the owner).
        """
        try:
            # Fetch the item by ID
            item = Item.objects.get(id=item_id)

            # Check if the authenticated user is the seller/owner of the item
            if item.seller != request.user:
                raise PermissionDenied("You do not have permission to delete this item.")

            # Delete the item if permission is granted
            item.delete()

            # Return a success response
            return Response({"message": "Item deleted successfully."}, status=status.HTTP_200_OK)

        except Item.DoesNotExist:
            # Return a 404 if the item does not exist
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        except PermissionDenied:
            # Return a 403 if the user does not have permission
            return Response({"error": "You do not have permission to delete this item."}, status=status.HTTP_403_FORBIDDEN)