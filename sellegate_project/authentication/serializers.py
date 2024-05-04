# authentication/serializers.py

from rest_framework import serializers
from .models import User
from evaluation.serializers import EvaluatorProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    # Define a write-only password field
    password = serializers.CharField(write_only=True)
    evaluatorProfile = EvaluatorProfileSerializer(source='evaluatorprofile', read_only=True)  # Nested serializer


    class Meta:
        model = User
        # Define the fields to include in the serialization
        fields = ('id', 'username', 'email', 'password', 'is_evaluator', 'evaluatorProfile', 'date_joined')
        read_only_fields = ('id', 'date_joined')  # Immutable fields


    def create(self, validated_data):
        # Extract and remove the password from the validated data
        password = validated_data.pop('password', None)

        # Create the user without password first to avoid exposing it in the serialized output
        user = User.objects.create(**validated_data)

        # Set the password separately to trigger hashing
        if password:
            user.set_password(password)
            user.save()

        return user
    
    def update(self, instance, validated_data):
        print(validated_data)
        # Handle password separately
        if 'password' in validated_data:
            # Hash the password before setting it
            instance.set_password(validated_data.pop('password'))

        # Perform default update for other fields
        return super().update(instance, validated_data)
