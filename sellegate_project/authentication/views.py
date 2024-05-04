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
from evaluation.models import EvaluatorProfile


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
    """
    API endpoint to create a new user (sign-up) and return the user with a token and evaluatorProfile.
    """
    permission_classes = [AllowAny]  # Allow public access, no token required

    def post(self, request):
        """
            ### User Sign-Up with Postman

            To register a new user with the sign-up API, follow these steps:

            1. **Set HTTP Method to POST**:
            - In Postman, select `POST` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Use the endpoint for user registration, typically: `http://localhost:8000/auth/register/`.

            3. **Set the Headers**:
            - You don't need any special headers for sign-up (no `Authorization` is required).

            4. **Set the Request Body**:
            - Click on the "Body" tab.
            - Choose `raw` and set the data format to `JSON`.
            - Add the key-value pairs for user registration:
                ```json
                {
                "username": "your_username",
                "email": "your_email@example.com",
                "password": "your_password"
                }
                ```

            5. **Send the Request**:
            - Click "Send" to submit the request.
            - If successful, you'll receive a `201 Created` response with the following data structure:
                ```json
                {
                "id": 1,  # User ID
                "username": "your_username",
                "email": "your_email@example.com",
                "is_evaluator": false,  # Default value
                "token": "your_token_here",  # Use this for future authenticated requests
                "evaluatorProfile": {
                    "bio": ""  # Default empty string
                }
                }
                ```

            6. **Handling Errors**:
            - If the registration fails, you'll receive a `400 Bad Request` response with a consistent error message structure:
                ```json
                {
                "status": "error",
                "error": {
                    "message": "Validation failed",
                    "details": {
                    "username": ["This field is required."],  # Example error details
                    "email": ["This field is required."]
                    }
                }
                }
                ```

            7. **Use the Token**:
            - If registration is successful, keep the token for future authenticated requests.
            - Include it in the `Authorization` header as `Token your_token_here`.
            """
        # Deserialize the request data
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new user
            user = serializer.save()

            # Create a token for the new user
            token, _ = Token.objects.get_or_create(user=user)

            # Construct response data with the expected structure
            response_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_evaluator': False,
                'token': token.key,
                'evaluatorProfile': {'bio': ''},  # Default bio
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # Consistent error structure for validation errors
        error_response = {
            'status': 'error',
            'error': {
                'message': 'Validation failed',
                'details': serializer.errors
            }
        }

        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


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
