# evaluation/serializers.py

from rest_framework import serializers
from .models import Evaluation
from item_management.models import Item
from item_management.serializers import ItemSerializer

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'  # You can customize this based on your requirements

class AssessmentRequestSerializer(serializers.Serializer):
    itemId = serializers.IntegerField()
    evaluatorId = serializers.IntegerField()
    message = serializers.CharField(max_length=255)
    item = ItemSerializer()  # Include ItemSerializer as a field if necessary