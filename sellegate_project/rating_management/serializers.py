from rest_framework import serializers
from .models import EvaluatorRating, SellerRating

class EvaluatorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorRating
        fields = '__all__'

class SellerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerRating
        fields = '__all__'
