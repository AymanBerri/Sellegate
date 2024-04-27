# authentication/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer


class UserDetailAPIView(APIView):
    # Require authentication
    permission_classes = [IsAuthenticated] #Currently any authenticated user can get any other user. We can add more constrains later

    def get(self, request, id):
        # Retrieve the user by ID, or return 404 if not found
        user = get_object_or_404(User, id=id)
        
        # Serialize user details for the response
        user_serializer = UserSerializer(user)
        
        # Return serialized user data
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]  # Allow public access, no token required

    def post(self, request):
        """
            ### Registering a User with Postman (Form Data)

            To send a POST request to register a user in Postman:

            1. **Set the HTTP Method to POST**:
            - Select `POST` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Type the endpoint for user registration, like `http://localhost:8000/auth/register/`.

            3. **Set the Headers**:
            - `Authorization` is not needed for registration.
            - Postman will set `Content-Type` automatically for form data.

            4. **Set the Request Body**:
            - Click on the "Body" tab.
            - Add key-value pairs for form data, as needed for registration. Example:
                - `username`: `"new_username"`
                - `email`: `"your_email@example.com"`
                - `password`: `"your_password"`

            5. **Send the Request**:
            - Click "Send" to submit the request.
            - If successful, you'll receive a JSON response with user details and a token.
            - If registration fails, an error message will indicate validation errors or other issues.

            6. **Using the Token**:
            - If registration is successful, keep the token for future authenticated requests.
            - Use it in the `Authorization` header as `Token <your_token>`.
            """

        # Deserialize request data
        serializer = UserSerializer(data=request.data)
        
        # Check if serializer data is valid
        if serializer.is_valid():
            # Save user and generate token
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            # Construct response data
            response_data = {
                'userId': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key,
                'is_evaluator': user.is_evaluator
            }

            # Return success response
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]  # Allow public access, no token required

    def post(self, request):
        """
            ### Logging in with Postman (Form Data)

            To send a POST request for login using form data in Postman:

            1. **Set the HTTP Method to POST**:
            - Select `POST` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Type the URL for the login endpoint, like `http://localhost:8000/auth/login/`.

            3. **Set the Headers**:
            - No `Authorization` header is needed for login.
            - Postman will set `Content-Type` automatically for form data.

            4. **Set the Request Body**:
            - Click on the "Body" tab.
            - Add the key-value pairs for form data:
                - `email`: `"your_email@example.com"`
                - `password`: `"your_password"`

            5. **Send the Request**:
            - Click "Send" to submit the request.
            - If successful, you'll receive a JSON response with a token and user info.
            - If login fails, an error message will indicate why.

            6. **Using the Token**:
            - If login is successful, keep the token for future authenticated requests.
            - Use it in the `Authorization` header as `Token <your_token>`.
        """


        # Extract email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Received email: {email}, password: {password}")

        # Fetch username based on email
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            # Return error response if user with the provided email does not exist
            print("User with the provided email does not exist")
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate user using fetched username and password
        user = authenticate(username=username, password=password)

        if user is not None:
            print(f"Authentication successful: {user.username} ({user.email})")
            
            # Delete previous tokens for the user, to enfore one token practice
            # Token.objects.filter(user=user).delete()

            # Generate new token
            token, _ = Token.objects.get_or_create(user=user)

            # Construct response data
            response_data = {
                'userId': user.id,
                'username': user.username,
                'email': user.email,
                'is_evaluator': user.is_evaluator,
                'token': token.key
            }

            # Return success response
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            print("Authentication failed")

            # Return error response for authentication failure
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        '''
        Logout a user using powershell console:
            Invoke-RestMethod -Method Post -Uri "http://localhost:8000/auth/logout/" -Headers @{ "Authorization" = "Token <your_token_here>" }
            Invoke-RestMethod -Method Post -Uri "http://localhost:8000/auth/logout/" -Headers @{ "Authorization" = "Token 71c2fa175cf0b2e8f73ed7ba20ee65d2870c9e5c" }
        '''


        try:
            # Get the user's email
            user_email = request.user.email
            
            # Attempt to delete the token
            request.user.auth_token.delete()
            
            # Return a success response upon successful logout, including the user's email
            return Response({"detail": f"Logout successful for user {user_email}."}, status=status.HTTP_200_OK)
        except Exception as e:
            # Return an error response if token deletion fails
            return Response({"detail": "Failed to log out."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # Summary:
    # In token-based authentication systems, typically, a new token is issued for 
        # each session or login event. This means that each time a user logs in, a 
        # new token is generated and associated with that specific session or login 
        # event. This ensures that the token remains unique to that particular 
        # session or login instance.

    # This view handles the logout process for authenticated users.
        # When a user sends a POST request to this endpoint, their authentication token
        # is deleted, effectively logging them out. Since tokens are stateless and used
        # for authentication, deleting the token invalidates the user's session,
        # requiring them to authenticate again for future requests.
