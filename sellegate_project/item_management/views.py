from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Item, Purchase
from .serializers import ItemSerializer, PurchaseSerializer
from rest_framework.filters import SearchFilter, OrderingFilter




class PurchaseItemAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    
    def post(self, request, format=None):
        """
        Purchase an item directly.
        """
        # Extract data from the request body
        item_id = request.data.get('itemId')
        quantity = request.data.get('quantity')
        
        # Get the authenticated user making the request
        # In this view the person making the request is the Buyer. If desired otherwise, defining whom the
        # buyer is, adding the buyer_id to the request payload and modifying the view is mandatory.
        buyer = request.user  # Assuming user is authenticated
        
        # Fetch the item from the database
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the item's delegation state allows purchase
        if item.delegation_state not in ['Approved', 'Independent']:
            return Response({"error": f"Item cannot be purchased due to delegation state, presently {item.delegation_state}"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price
        total_price = item.price * quantity

        # Create a new purchase with the buyer set
        purchase = Purchase.objects.create(item=item, buyer=buyer, quantity=quantity, total_price=total_price)

        # Serialize the purchase data
        serializer = PurchaseSerializer(purchase)

        # Return the response
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ItemListCreateAPIView(APIView):

    def post(self, request, format=None):
        """
        Create a new item.

        Example payload:
        {
            "seller_id": 26,
            "title": "New Item",
            "description": "Description of the item",
            "price": "99.99",
            "category": "Electronics",
            "delegation_state": "Pending"
        }
        """

         # Create a serializer instance with the request data
        serializer = ItemSerializer(data=request.data)

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
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]  # Add filter backends for search and ordering

    search_fields = ['title', 'description', 'seller__username']  # Specify fields for search
    ordering_fields = ['price']  # Specify fields for ordering

    def get_queryset(self):
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
    def get(self, request, itemId, format=None):
        try:
            item = Item.objects.get(pk=itemId)  # Retrieve the item by its ID
            serializer = ItemSerializer(item)  # Serialize the item
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return the serialized data
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)  # Return 404 if item is not found