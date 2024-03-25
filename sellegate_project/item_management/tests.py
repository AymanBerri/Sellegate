from authentication.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from .models import Item

class ItemListCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user who will be the seller
        self.user = User.objects.create_user(username='seller', password='password')
        self.token = Token.objects.create(user=self.user)

        # Authenticate the client with the user's token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_item(self):
        # Define the data for the new item
        data = {
            'userId': self.user.id,
            'title': 'New Item',
            'description': 'Description of the item',
            'price': '99.99',
            'category': 'Electronics',
            'delegationState': 'Pending'
        }

        # Make a POST request to create the item
        response = self.client.post('/items/list/', data, format='json')

        # Print out response data and errors for debugging
        print(response.data)
        print(response.data['errors'] if 'errors' in response.data else None)

        # Check that the request was successful (status code 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the item was created in the database
        self.assertTrue(Item.objects.filter(title='New Item').exists())