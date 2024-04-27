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



class PurchaseItemAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    
    # def post(self, request, format=None):
    #     """
    #         ### Purchasing an Item with Postman

    #         To send a POST request to purchase an item using form data in Postman, follow these steps:

    #         1. **Set the HTTP Method to POST**:
    #         - Select `POST` from the method dropdown.

    #         2. **Enter the Endpoint URL**:
    #         - Use the URL for the purchase endpoint. Example: `http://localhost:8000/api/purchase/`.

    #         3. **Set the Headers**:
    #         - Add the `Authorization` header with your token:
    #             - `Authorization`: `Token <your_token_here>`  # Replace with your actual token

    #         4. **Set the Request Body**:
    #         - Click on the "Body" tab.
    #         - Choose `form-data`.
    #         - Add the following key-value pairs for purchasing an item:
    #             - `item_id`: `1`  # ID of the item you want to purchase
    #             - `quantity`: `2`  # Number of units to purchase (REMOVED FOR NOW AS PER REQUIRMENTS)

    #         5. **Send the Request**:
    #         - Click "Send" to submit the POST request.
    #         - If successful, you should get a 201 Created response with the purchase details.
    #         - If the request fails, check the response for error messages.

    #         6. **Common Error Responses**:
    #         - **400 Bad Request**: If `item_id` or `quantity` cannot be converted to an integer, or if the item isn't purchasable due to delegation state.
    #         - **404 Not Found**: If the specified item does not exist.

    #     """
    #     # if 'item_id' not in request.data:
    #     #     return Response({"error": "item_id is required."}, status=status.HTTP_400_BAD_REQUEST)


    #     # Extract data from the request body
    #     try:
    #         item_id = int(request.data.get('item_id'))
    #     except (TypeError, ValueError):
    #         # Return a 400 Bad Request response if the conversion fails
    #         return Response({"error": "Invalid item_id. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # quantity = int(request.data.get('quantity'))
    #         quantity = 1
    #     except (TypeError, ValueError):
    #         # Return a 400 Bad Request response if the conversion fails
    #         return Response({"error": "Invalid quantity. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Get the authenticated user making the request
    #     # In this view the person making the request is the Buyer. If desired otherwise, defining whom the
    #     # buyer is, adding the buyer_id to the request payload and modifying the view is mandatory.
    #     buyer = request.user  # Assuming user is authenticated
        
    #     # Fetch the item from the database
    #     try:
    #         item = Item.objects.get(id=item_id)
    #     except Item.DoesNotExist:
    #         return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        
    #     # Check if the item is sold or not visible
    #     # if item.is_sold:
    #     #     return Response({"error": "This item has already been sold."}, status=status.HTTP_400_BAD_REQUEST)
    #     # if not item.is_visible:
    #     #     return Response({"error": "This item is not visible and cannot be purchased."}, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Check if the item's delegation state allows purchase
    #     if item.delegation_state not in ['Approved', 'Independent']:
    #         return Response({"error": f"Item cannot be purchased due to delegation state, presently {item.delegation_state}"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Calculate total price
    #     total_price = item.price * quantity

    #     # Create a new purchase with the buyer set
    #     purchase = Purchase.objects.create(item=item, buyer=buyer, quantity=quantity, total_price=total_price)

    #     # Update item status after purchase
    #     item.is_sold = True  # Mark item as sold
    #     item.is_visible = False  # Set item to not be visible
    #     item.save()  # Save the changes to the database

    #     # Serialize the purchase data
    #     serializer = PurchaseSerializer(purchase)

    #     # Return the response
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, format=None):
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
            ### Creating an Item with Postman (Form Data)

            To create a new item in Postman using form data, follow these steps:

            1. **Set the HTTP Method to POST**:
            - Select `POST` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Use the URL for creating an item. Example: `http://localhost:8000/items/`.

            3. **Set the Headers**:
            - Add the `Authorization` header with your authentication token:
                - `Authorization`: `Token <your_token_here>`  # Replace with your token
            - If using form data, Postman will automatically set the `Content-Type`.

            4. **Set the Request Body**:
            - Click on the "Body" tab.
            - Choose `form-data`.
            - Add the key-value pairs to create a new item. Ensure all required fields are provided:
                - `title`: `"Item Title"`  # Required
                - `description`: `"Item Description"`  # Required
                - `price`: `"99.99"`  # Required (Use appropriate price format)
                - `delegation_state`: `"Pending"`  # Required (Choose from defined states)
                - `is_visible`: `"true"`  # Required (Must be provided explicitly)
            - Optional fields, if needed:
                - `thumbnail_url`: `"http://example.com/image.jpg"`  # Optional thumbnail image URL

            5. **Send the Request**:
            - Click "Send" to submit the request.
            - If successful, you'll receive a `201 Created` response with the serialized item data.
            - If there's an error, check the response body for validation errors or other issues.

            6. **Handling Errors**:
            - If you get a `400 Bad Request` response, examine the response body to understand which fields are missing or invalid.
            - Ensure all required fields are included in the request body. 

            7. **Seller ID Handling**:
            - The `seller_id` is set automatically based on the authenticated user. It is not required in the request payload.

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