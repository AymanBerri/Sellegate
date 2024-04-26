# In evaluation/serializers.py

from rest_framework import serializers
from .models import Evaluator

class EarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluator
        fields = ['total_earnings', 'evaluations']

class EvaluatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluator
        fields = ['experience', 'description']
