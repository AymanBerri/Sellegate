# item_management/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Item, Payment
from decimal import Decimal
import json

User = get_user_model()

class ItemManagementTests(APITestCase):

    def setUp(self):
        # Create test users and tokens
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='SellerPass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='BuyerPass123'
        )

        self.client = APIClient()

    ### ITEM TESTS ###

    def test_create_item(self):
        # Set authentication to the seller
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.seller))

        # Data for creating an item
        data = {
            'title': 'Test Item',
            'description': 'This is a test item.',
            'price': '49.99',
            'thumbnail_url': None,
            'delegation_state': 'Pending',
            'is_visible': True,
        }

        url = reverse('post-item')
        response = self.client.post(url, data, format='json')

        # Assert successful creation of the item
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('item', response.data)
        self.assertEqual(response.data['item']['title'], 'Test Item', "Item title doesn't match")
    
    def test_get_all_items(self):
        # Create a few test items
        Item.objects.create(
            title='Item 1',
            description='Description for item 1',
            price=Decimal('10.00'),
            seller=self.seller,
            delegation_state='Pending',
            is_visible=True,
        )
        
        url = reverse('get-all-items')
        response = self.client.get(url, format='json')

        # Assert successful retrieval of items
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0, "No items returned")
    
    def test_get_user_products(self):
        # Create an item for the seller
        item = Item.objects.create(
            title='Seller Item',
            description='Item owned by seller',
            price=Decimal('29.99'),
            seller=self.seller,
            delegation_state='Pending',
            is_visible=True,
        )

        # Authenticate as the seller
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.seller))
        
        url = reverse('get-user-products')
        response = self.client.get(url, format='json')

        # Assert successful retrieval of seller's items
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1, "Unexpected number of items returned")

    def test_update_item(self):
        # Create a test item
        item = Item.objects.create(
            title='Old Title',
            description='Old Description',
            price=Decimal('29.99'),
            seller=self.seller,
            delegation_state='Pending',
            is_visible=True,
        )

        # Authenticate as the seller
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.seller))
        
        # Update data
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }

        url = reverse('update-item', args=[item.id])
        response = self.client.patch(url, update_data, format='json')

        # Assert successful update of the item
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item']['title'], 'Updated Title', "Title wasn't updated")
        self.assertEqual(response.data['item']['description'], 'Updated Description', "Description wasn't updated")
    
    def test_delete_item(self):
        # Create a test item
        item = Item.objects.create(
            title='Item to Delete',
            description='Item to be deleted',
            price=Decimal('29.99'),
            seller=self.seller,
            delegation_state='Pending',
            is_visible=True,
        )

        # Authenticate as the seller
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.seller))

        url = reverse('delete-item', args=[item.id])
        response = self.client.delete(url)

        # Assert successful deletion of the item
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Item with ID' in response.data['message'], "Item deletion message incorrect")

    ### PAYMENT TESTS ###

    def test_buy_item(self):
        # Create a test item
        item = Item.objects.create(
            title='Item to Buy',
            description='Item available for purchase',
            price=Decimal('49.99'),
            seller=self.seller,
            delegation_state='Pending',
            is_visible=True,
        )

        # Authenticate as the buyer
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.buyer))

        url = reverse('buy-item', args=[item.id])
        response = self.client.post(url)

        # Assert successful purchase and payment record creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('payment' in response.data, "Payment record not created after buying item")
        self.assertEqual(response.data['payment']['item_name'], 'Item to Buy', "Payment details incorrect")

    def test_get_user_payments(self):
        # Create a payment for the buyer
        item = Item.objects.create(
            title='Item for Payment Test',
            description='Test item for payment',
            price=Decimal('49.99'),
            seller=self.seller,
            delegation_state='Pending',
            is_visible=True,
        )
        payment = Payment.objects.create(
            item=item,
            buyer=self.buyer,
            total_price=item.price,
        )

        # Authenticate as the buyer
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.buyer))

        url = reverse('get-user-payments')
        response = self.client.get(url, format='json')

        # Assert successful retrieval of user payments
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0, "No payments found for the user")

    ### HELPER FUNCTIONS ###

    def _get_user_token(self, user):
        """
        Helper function to retrieve or create a token for a given user.
        """
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
