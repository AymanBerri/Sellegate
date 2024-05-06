# tests.py
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from authentication.views import UserLogoutAPIView


User = get_user_model()

class AuthenticationTests(APITestCase):

    def setUp(self):
        # Create a test user and token
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPassword123'
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)

        # Set up the APIClient
        self.client = APIClient()  # Create an instance of APIClient for making requests

    def test_user_registration(self):
        # Test user registration with valid data
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewUserPass123'
        }
        url = reverse('user-registration')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_user_registration_invalid_data(self):
        # Test registration with invalid data (e.g., missing password)
        data = {
            'username': 'invaliduser',
            'email': 'invaliduser@example.com',
            'password': ''
        }
        url = reverse('user-registration')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        # Test successful login with correct credentials
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123'
        }
        url = reverse('user-login')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_invalid(self):
        # Test login with incorrect password
        data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword'
        }
        url = reverse('user-login')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        # Set the token in the client's credentials
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Call the logout endpoint
        url = reverse('user-logout')
        response = self.client.post(url)

        # Assert that the logout was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Logout failed: {response.data}")

    def test_unauthorized_access(self):
        # Test access without token
        self.client.credentials()  # Clear the credentials
        url = reverse('user-logout')
        response = self.client.post(url)

        # Assert that the unauthorized access is handled
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "Unauthorized access should be denied")

    def test_user_detail(self):
        # Test fetching user details with token-based authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Set the token for authentication
        
        # Get the URL for the user detail endpoint
        url = reverse('user_detail', args=[self.user.id])
        
        # Make a GET request to fetch user details
        response = self.client.get(url)
        
        # Assert that the response status code is 200 (OK), indicating successful authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Failed to fetch user details")
        
        # Assert that the response contains the expected user information (e.g., email)
        self.assertIn('email', response.data)

    def test_user_update(self):
        # Authenticate using the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Endpoint for updating user information
        url = reverse('update-user')

        # Data to update the user
        update_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }

        # Send a PATCH request to update user information
        response = self.client.patch(url, update_data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to update user information: {response.data}")

        # Check if the 'user' key is in the response
        if 'user' not in response.data:
            self.fail("The response did not contain expected user data")

        # Extract the user data from the response
        user_data = response.data['user']

        # Validate the updated username
        self.assertEqual(user_data['username'], 'updateduser', "Username was not updated")
        
        # Validate the updated email
        self.assertEqual(user_data['email'], 'updated@example.com', "Email was not updated")