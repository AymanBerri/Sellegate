# authentication/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                "userId": user.id,
                "username": user.username,
                "email": user.email,
                "token": token.key
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                "userId": user.id,
                "username": user.username,
                "email": user.email,
                "token": token.key
            }
            return Response(response_data)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
