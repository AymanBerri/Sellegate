# evaluation/serializers.py

from rest_framework import serializers
from item_management.models import Item
from .models import EvaluatorProfile, EvaluationRequest

from authentication.models import User  # Import the User model


class EvaluatorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for EvaluatorProfile.
    """
    class Meta:
        model = EvaluatorProfile
        fields = ['bio']  # Currently, just the bio
        

class EvaluationRequestSerializer(serializers.ModelSerializer):
    # Expecting primary key for the item field, with validation
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    
    # Use ReadOnlyField to derive evaluator_id from the evaluator's ID
    evaluator_id = serializers.ReadOnlyField(source="evaluator.id")  # Read-only field for evaluator's ID

    class Meta:
        model = EvaluationRequest
        fields = ['id', 'item_id', 'evaluator_id', 'message', 'status', 'request_date']
