from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from item_management.models import Item
from item_management.serializers import ItemSerializer

from .models import EvaluationRequest
from .serializers import EvaluationRequestSerializer

# Create your views here.

class SearchItemsToEvaluateAPIView(APIView):
    def get(self, request):
        """
        Get a list of items that are pending evaluation.
        ### Fetching Items Pending Evaluation with Postman

        To retrieve a list of items pending evaluation in Postman, follow these steps:

        1. **Set the HTTP Method to GET**:
        - Select `GET` from the method dropdown.

        2. **Enter the Endpoint URL**:
        - Use the endpoint for fetching items pending evaluation. Example: `http://localhost:8000/evaluation/items/`.

        3. **Set the Headers**:
        - If required, add the `Authorization` header with your token:
            - `Authorization`: `Token <your_token_here>`  # Replace with your token

        4. **Send the Request**:
        - Click "Send" to submit the GET request.
        - If successful, you should get a 200 OK response with a list of items pending evaluation.
        - If there are no pending items, you might receive a 404 Not Found with a suitable message.

        5. **Common Error Responses**:
        - **404 Not Found**: This can occur if there are no items with `delegation_state` of 'Pending'.
        - **403 Forbidden**: This can happen if the endpoint requires authentication or permission that isn't provided.

        """
        # Fetch items with delegation_state 'Pending'
        items = Item.objects.filter(delegation_state='Pending')

        if not items.exists():
            # If no items are pending evaluation, return a suitable response
            return Response(
                {"message": "No items pending evaluation at this time."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the items
        serializer = ItemSerializer(items, many=True)

        # Return the serialized data with a success message
        return Response(
            {
                "message": f"Found {len(items)} items pending evaluation.",
                "items": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    


# MUST RETURN EVALUATOR ID, FIX IT
class SendItemAssessmentRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure the authenticated user is an evaluator
        if not request.user.is_evaluator:
            return Response(
                {"error": "Only evaluators can send assessment requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        item_id = request.data.get("item_id")
        message = request.data.get("message", "")

        if not item_id:
            return Response(
                {"error": "item_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            item = Item.objects.get(id=item_id)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Item not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Provide necessary data to the serializer
        data = {
            "item_id": item_id,  # Item primary key
            "message": message,  # Optional message
        }

        # Use the serializer to validate and create the evaluation request
        serializer = EvaluationRequestSerializer(data=data)

        if serializer.is_valid():
            # Save with the authenticated user as the evaluator
            evaluation_request = serializer.save(
                item=item,
                evaluator=request.user,  # Manually set the evaluator to the authenticated user
                status="requested",  # Set the status to 'requested'
            )

            # Serialize the response to ensure the correct data is returned
            response_serializer = EvaluationRequestSerializer(evaluation_request)

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)