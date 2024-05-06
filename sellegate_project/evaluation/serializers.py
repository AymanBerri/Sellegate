# evaluation/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from item_management.models import Item
from .models import EvaluatorProfile, EvaluationRequest, EvaluationRequest

# from authentication.models import User  # Import the User model
User = get_user_model()

class EvaluationRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving AssessmentRequest data with evaluator_id.
    """
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),  # Ensures valid items are referenced
        source='item'
    )

    evaluator_id = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        source='evaluator'  # Maps to the underlying 'evaluator' ForeignKey
    )

    created_at = serializers.SerializerMethodField()  # Method for formatted creation date

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d")  # Custom date formatting

    class Meta:
        model = EvaluationRequest
        fields = [
            'id',  # ID of the assessment request
            'item_id',  # Reference to the item being assessed
            'evaluator_id',  # ID of the evaluator
            'name',  # Title of the message
            'message',  # Assessment message
            'price',  # New estimated price
            'state',  # Defaults to 'Pending'
            'created_at',  # Formatted creation date
        ]
        read_only_fields = ['id', 'evaluator_id', 'state', 'created_at']  # Ensure these are not editable

    def create(self, validated_data):
        """
        Create a new assessment request with the current logged-in user as the evaluator.
        """
        user = self.context['request'].user  # Current user (evaluator)
        validated_data['evaluator'] = user  # Set the evaluator to the current user
        
        # Set default state to 'Pending'
        validated_data['state'] = 'Pending'
        
        return EvaluationRequest.objects.create(**validated_data)  # Create and return the new assessment request




class EvaluatorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for EvaluatorProfile.
    """
    class Meta:
        model = EvaluatorProfile
        fields = ['bio']  # Currently, just the bio
        
# OLD \/\/\///\/\/\///\/\/\/\/\/\/

class _EvaluationRequestSerializer(serializers.ModelSerializer):
    # Expecting primary key for the item field, with validation
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    
    # Use ReadOnlyField to derive evaluator_id from the evaluator's ID
    evaluator_id = serializers.ReadOnlyField(source="evaluator.id")  # Read-only field for evaluator's ID

    class Meta:
        model = EvaluationRequest
        fields = ['id', 'item_id', 'evaluator_id', 'message', 'status', 'request_date']


