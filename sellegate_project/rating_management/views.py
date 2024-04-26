from django.shortcuts import render
from .models import EvaluatorRating, SellerRating
from django.http import JsonResponse
from .serializers import EvaluatorRatingSerializer, SellerRatingSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def rate_evaluator(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EvaluatorRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def rate_seller(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SellerRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
