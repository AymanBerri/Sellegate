# authentication/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # Define a write-only password field
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Define the fields to include in the serialization
        fields = ('id', 'username', 'email', 'password', 'is_evaluator', 'date_joined')

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