# evaluation/serializers.py

from rest_framework import serializers
from .models import Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'  # You can customize this based on your requirements
