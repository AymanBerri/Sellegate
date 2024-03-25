from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Item
from .serializers import ItemSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

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