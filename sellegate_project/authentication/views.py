# authentication/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer
from evaluation.models import EvaluatorProfile
from evaluation.serializers import EvaluatorProfileSerializer


# ERROR RESPONSE FORMAT:
    # {
    #   "status": "error",
    #   "error": {
    #     "message": "A brief, clear error message",
    #     "code": 400,  # HTTP status code (400, 403, 404, etc.)
    #     "details": {
    #       "field_name": ["Error detail 1", "Error detail 2"],
    #       "another_field": ["Error message for this field"]
    #     }
    #   }
    # }

class TokenStatusAPIView(APIView):
    """
    API endpoint to return user details if the token is valid.
    """
    permission_classes = [IsAuthenticated]  # Require authentication to access the endpoint

    def get(self, request):
        # Get the current user from the request
        user = request.user
        
        # Find the token for the current user
        token = Token.objects.filter(user=user).first()

        if token:
            # If the token exists, return user details and the token
            user_serializer = UserSerializer(user)
            response_data = user_serializer.data
            response_data['token'] = token.key

            return Response(
                {
                    "message": "Token is valid.",
                    "user_details": response_data,
                },
                status=status.HTTP_200_OK
            )
        else:
            pass
            # Django habdles cases wherethe token does not exist, or if no token was passed.

        

class UserDetailAPIView(APIView):
    # Require authentication
    permission_classes = [IsAuthenticated] #Currently any authenticated user can get any other user. We can add more constrains later

    def get(self, request, id):
        """
            ### Fetching User Details by ID with Postman

            To fetch user details using Postman, follow these steps:

            1. **Set HTTP Method to GET**:
            - Select `GET` from the method dropdown.

            2. **Enter the Endpoint URL**:
            - Use the URL for retrieving user details by ID. Example: `http://localhost:8000/user/1/`.
            - Replace `1` with the desired user ID.

            3. **Set the Headers**:
            - Add the `Authorization` header with your authentication token:
                - `Authorization`: `Token <your_token_here>`  # Replace `<your_token_here>` with your actual token

            4. **Send the Request**:
            - Click "Send" to submit the GET request.
            - If successful, you'll receive a `200 OK` response with the serialized user data. The expected fields include `id`, `username`, `email`, `is_evaluator`, `evaluatorProfile`, etc.

            5. **Handling Errors and Feedback**:
            - **404 Not Found**: If the user with the specified ID does not exist, you'll get a 404 response with an appropriate error message.
            - **403 Forbidden**: If you don't have permission to view the user's details, you'll get a 403 response with an error message.

            ### Example Response for a Successful Request
            ```json
            {
            "id": 1,
            "username": "example_user",
            "email": "example@example.com",
            "is_evaluator": false,
            "evaluatorProfile": {
                "bio": ""
            }
            }
            """
        # Retrieve the user by ID, or return 404 if not found
        user = get_object_or_404(User, id=id)
        
        # Serialize user details for the response
        user_serializer = UserSerializer(user)
        
        # Return serialized user data
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class UpdateUserAPIView(APIView):
    """
    API endpoint to update the current logged-in user's information.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        # Get the authenticated user
        user = request.user

        # Define immutable fields that cannot be updated
        immutable_fields = {'id', 'date_joined'}

        # Check if any immutable fields are being updated
        if any(key in immutable_fields for key in request.data):
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": f"Cannot update immutable fields: {', '.join(immutable_fields)}",
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Define allowed keys for update
        allowed_keys = {'username', 'email', 'password', 'evaluatorProfile'}

        # Check for invalid keys
        invalid_keys = [key for key in request.data if key not in allowed_keys]

        if invalid_keys:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": f"Invalid key(s) in request data: {', '.join(invalid_keys)}",
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for evaluator profile data
        evaluator_profile_data = request.data.get("evaluatorProfile", None)
        
        # Initialize the UserSerializer with partial updates
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        # Validate the serializer
        if not user_serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "Validation failed for user data",
                        "details": user_serializer.errors,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the valid user data
        updated_user = user_serializer.save()

        # Handle updates for evaluator profile
        if evaluator_profile_data:
            evaluator_profile = user.evaluatorprofile  # Get the evaluator profile instance
            evaluator_profile_serializer = EvaluatorProfileSerializer(
                evaluator_profile,
                data=evaluator_profile_data,
                partial=True,
            )

            if not evaluator_profile_serializer.is_valid():
                return Response(
                    {
                        "status": "error",
                        "error": {
                            "message": "Validation failed for evaluator profile",
                            "details": evaluator_profile_serializer.errors,
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            evaluator_profile_serializer.save()  # Save valid evaluator profile data

        # Return success response with updated user data
        return Response(
            {
                "message": "User updated successfully.",
                "user": UserSerializer(updated_user).data,
            },
            status=status.HTTP_200_OK,
        )

class UserRegistrationAPIView(APIView):
    """
    API endpoint to create a new user (sign-up) and return a token.
    """
    permission_classes = [AllowAny]  # Allow public access for registration
    authentication_classes = []  # No authentication required

    def post(self, request):
        # Use the serializer to validate and create the user
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Save the user and ensure any necessary signals (like profile creation) are triggered
            user = serializer.save()

            # Create a token for the new user
            token, created = Token.objects.get_or_create(user=user)

            # Serialize the user to get the structured response
            user_serializer = UserSerializer(user)

            # Construct the response data including the token
            response_data = user_serializer.data
            response_data['token'] = token.key  # Include the generated token

            return Response(response_data, status=status.HTTP_201_CREATED)

        # Handle validation errors
        error_response = {
            'status': 'error',
            'error': {
                'message': 'Validation failed',
                'details': serializer.errors,
            },
        }

        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]  # Allow public access, no token required
    authentication_classes = []


    def post(self, request):
        # Extract email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Fetch the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return error response if the user with the provided email does not exist
            return Response(
                {
                    'status': 'error',
                    'error': {
                        'message': 'Invalid credentials: User with the provided email does not exist.'
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate the user with the provided password
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is not None:
            # Create or get a token for the authenticated user
            token, _ = Token.objects.get_or_create(user=authenticated_user)

            # Serialize the user data
            serialized_user = UserSerializer(authenticated_user)

            # Include the token in the serialized data
            response_data = {
                **serialized_user.data,
                'token': token.key  # Add the token to the response
            }

            # Return success response with the serialized user data and token
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            # Return error response if authentication fails
            return Response(
                {
                    'status': 'error',
                    'error': {
                        'message': 'Invalid credentials: Incorrect password.'
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
    
class UserLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):

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
