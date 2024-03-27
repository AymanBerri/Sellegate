from django.shortcuts import render
from . import models

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer
from item_management.models import Item

# Create your views here.

class AddToCartAPIView(APIView):
    def post(self, request, format=None):
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