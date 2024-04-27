from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from item_management.models import Item
from item_management.serializers import ItemSerializer


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
        - `Content-Type` is generally set to `application/json` for GET requests.

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