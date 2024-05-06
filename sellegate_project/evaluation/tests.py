# evaluation/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from item_management.models import Item
from .models import EvaluationRequest, EvaluatorProfile
from decimal import Decimal

User = get_user_model()

class EvaluationTests(APITestCase):

    def setUp(self):
        # Create test users and items
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='SellerPass123'
        )
        self.evaluator = User.objects.create_user(
            username='evaluator',
            email='evaluator@example.com',
            password='EvaluatorPass123',
            is_evaluator=True
        )

        self.client = APIClient()

        # Create a test item owned by the seller
        self.test_item = Item.objects.create(
            title='Test Item',
            description='Test item for evaluation',
            price=Decimal('49.99'),
            seller=self.seller,
            delegation_state='Pending',
            is_visible=True,
        )

    ### EVALUATION REQUEST TESTS ###

    def test_send_evaluation_request(self):
        # Authenticate as the evaluator
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.evaluator))
        
        # Data for the evaluation request
        data = {
            'item_id': self.test_item.id,
            'name': 'Item Evaluation',
            'message': 'Please evaluate this item.',
            'price': '55.00',
        }

        url = reverse('new-evaluation')
        response = self.client.post(url, data, format='json')

        # Assert successful creation of the evaluation request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('evaluation', response.data)
        self.assertEqual(response.data['evaluation']['name'], 'Item Evaluation', "Evaluation name doesn't match")
    
    def test_send_evaluation_request_unauthorized(self):
        # Authenticate as a non-evaluator
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.seller))
        
        data = {
            'item_id': self.test_item.id,
            'name': 'Unauthorized Evaluation',
            'message': 'This should not be allowed.',
            'price': '55.00',
        }

        url = reverse('new-evaluation')
        response = self.client.post(url, data, format='json')

        # Assert unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "Unauthorized user should not be able to send evaluation requests")

    def test_get_my_evaluations(self):
        # Create an evaluation request
        evaluation_request = EvaluationRequest.objects.create(
            item=self.test_item,
            evaluator=self.evaluator,
            name='Existing Evaluation',
            message='This is an existing evaluation request.',
            price=Decimal('55.00')
        )

        # Authenticate as the evaluator
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.evaluator))

        url = reverse('my-evaluations')
        response = self.client.get(url, format='json')

        # Assert successful retrieval of the evaluator's own evaluation requests
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Failed to retrieve evaluator's own evaluations")
        self.assertGreater(len(response.data), 0, "No evaluation requests found")
    
    def test_reject_evaluation(self):
        # Create an evaluation request
        evaluation_request = EvaluationRequest.objects.create(
            item=self.test_item,
            evaluator=self.evaluator,
            name='Pending Evaluation',
            message='This evaluation is pending.',
            price=Decimal('55.00')
        )

        # Authenticate as the seller
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.seller))
        
        url = reverse('reject-evaluation', args=[evaluation_request.id])
        response = self.client.patch(url, format='json')

        # Assert successful rejection of the evaluation request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'evaluation request rejected successfully.')
    
    def test_accept_evaluation(self):
        # Ensure the test item is created and exists
        self.assertIsNotNone(self.test_item, "Test item is not initialized properly in setUp()")

        # Create an evaluation request
        evaluation_request = EvaluationRequest.objects.create(
            item=self.test_item,
            evaluator=self.evaluator,
            name='Pending Evaluation',
            message='This evaluation is pending.',
            price=Decimal('55.00')
        )

        # Ensure the evaluation request is created
        self.assertIsNotNone(evaluation_request, "Evaluation request was not created properly")

        # Authenticate as the seller
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self._get_user_token(self.seller))

        # Send the patch request to accept the evaluation
        url = reverse('accept-evaluation', args=[evaluation_request.id])
        response = self.client.patch(url, format='json')

        # Assert successful acceptance of the evaluation request
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Failed to accept the evaluation request")
        self.assertIn("message", response.data, "Response should contain a success message")

        # Refresh the item to ensure it still exists after the patch
        refreshed_item = Item.objects.filter(id=self.test_item.id).first()  # Using .first() to avoid raising exceptions

        # Ensure the item wasn't deleted
        self.assertIsNotNone(refreshed_item, "Test item was deleted or not found after accepting evaluation")

        # Assert that the item's delegation state is updated to 'Approved'
        self.assertEqual(refreshed_item.delegation_state, 'Approved', "Item's delegation state was not updated correctly")


    ### HELPER FUNCTIONS ###

    def _get_user_token(self, user):
        """
        Helper function to retrieve or create a token for a given user.
        """
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
