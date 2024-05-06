from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from item_management.models import Item
from item_management.serializers import ItemSerializer

from .models import EvaluationRequest, EvaluationRequest
from .serializers import EvaluationRequestSerializer, EvaluationRequestSerializer

# Create your views here.

class SendEvaluationRequestAPIView(APIView):
    """
    API endpoint for sending an evaluation request.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can send requests
    
    def post(self, request):
        # Ensure the user is an evaluator
        if not request.user.is_evaluator:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "User is not authorized to send evaluation requests.",
                        "code": status.HTTP_403_FORBIDDEN,
                    },
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = EvaluationRequestSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Create a new evaluation request
            new_evaluation = serializer.save()

            return Response(
                {
                    "message": "evaluation request created successfully.",
                    "evaluation": serializer.data,  # Return serialized evaluation details
                },
                status=status.HTTP_201_CREATED,
            )
        
        # Return error response if validation fails
        return Response(
            {
                "status": "error",
                "error": {
                    "message": "Validation failed.",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetMyEvaluationsAPIView(APIView):
    """
    API endpoint to retrieve evaluation requests created by the current evaluator.
    """
    def get(self, request):
        # Check if the current user is an evaluator
        if not request.user.is_evaluator:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "Only evaluators can access evaluation requests.",
                        "code": status.HTTP_403_FORBIDDEN
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Retrieve evaluation requests created by the current evaluator
        evaluations = EvaluationRequest.objects.filter(evaluator=request.user)

        # Serialize the evaluation requests
        serializer = EvaluationRequestSerializer(evaluations, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetEvaluationRequestsOnMyProductAPIView(APIView):
    """
    API endpoint to retrieve all evaluation requests for a specific item owned by the current user.
    """
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    
    def get(self, request):
        """
        Handles GET requests to get all evaluation requests for a specific item owned by the current user.
        """
        # Extract itemId from the request data
        item_id = request.data.get("item_id")

        # Check if the itemId is provided
        if not item_id:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "item_id is required.",
                        "code": status.HTTP_400_BAD_REQUEST,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieve the item and check if it belongs to the current logged-in user
        try:
            item = Item.objects.get(id=item_id)
            if item.seller != request.user:
                return Response(
                    {
                        "status": "error",
                        "error": {
                            "message": "Item not owned by the current user.",
                            "code": status.HTTP_403_FORBIDDEN,
                        },
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "Item not found.",
                        "code": status.HTTP_404_NOT_FOUND,
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get all evaluation requests for this item
        evaluation_requests = EvaluationRequest.objects.filter(item=item)

        # Use the evaluationRequestSerializer to serialize the evaluation requests
        evaluation_requests_data = EvaluationRequestSerializer(evaluation_requests, many=True).data

        # Return the serialized evaluation requests
        return Response(
            {
                "evaluation_requests": evaluation_requests_data,  # List of evaluation requests
            },
            status=status.HTTP_200_OK,
        )


class RejectEvaluationAPIView(APIView):
    """
    API endpoint to reject an evaluation request.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, evaluation_id):
        # Try to get the evaluation request, catching 404 if not found
        try:
            evaluation = EvaluationRequest.objects.get(id=evaluation_id)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "Assessment request not found.",
                        "code": 404,
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the current user owns the item associated with the evaluation
        item = evaluation.item
        if item.seller != request.user:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "You do not own this item. Only the item owner can reject evaluations.",
                        "code": status.HTTP_403_FORBIDDEN,
                    },
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Update the state to 'Rejected'
        evaluation.state = 'Rejected'
        evaluation.save()  # Save the change

        return Response(
            {
                "message": "evaluation request rejected successfully."
            },
            status=status.HTTP_200_OK,
        )


class AcceptEvaluationAPIView(APIView):
    """
    API endpoint to accept an evaluation request and update the relevant item information.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can accept evaluations

    def patch(self, request, evaluation_id):
        # Try to get the evaluation request, catching 404 if not found
        try:
            evaluation = EvaluationRequest.objects.get(id=evaluation_id)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "Assessment request not found.",
                        "code": 404,
                    },
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the current user owns the item associated with the evaluation
        item = evaluation.item
        if item.seller != request.user:
            return Response(
                {
                    "status": "error",
                    "error": {
                        "message": "You do not own this item. Only the item owner can accept evaluations.",
                        "code": 403,
                    },
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Update the relevant item information based on the evaluation request
        item.price = evaluation.price  # Update the price with the evaluation's estimated price
        item.delegation_state = 'Approved'  # Change the item's delegation state to "Approved"
        # Update additional information if needed (like item name, description, etc.)
        item.save()  # Save the updated item

        # Update the state of the evaluation request to 'Approved'
        evaluation.state = 'Approved'
        evaluation.save()  # Save the updated evaluation state

        return Response(
            {
                "message": "Evaluation request approved, item information updated.",
            },
            status=status.HTTP_200_OK,
        )

# OLD \/\/\/\/\/\/\/\/\/\/

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
    
class ApprovedEvaluationRequestAPIView(APIView):
    """
    API endpoint to retrieve the approved evaluation request for a given item_id.
    If there are more than one approved request, return all with an error message.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id, format=None):
        """
        ### Fetching Approved Evaluation Requests by Item ID with Postman

        To fetch approved evaluation requests for a specific item ID, follow these steps:

        1. **Set HTTP Method to GET**:
        - Select `GET` from the method dropdown in Postman.

        2. **Enter the Endpoint URL**:
        - Use the URL for fetching approved evaluation requests by `item_id`. Example: `http://localhost:8000/evaluation/approved-evaluation/1/`.
        - Replace `1` with the desired item ID.

        3. **Set the Headers**:
        - Add the `Authorization` header with your authentication token:
            - `Authorization`: `Token <your_token_here>`  # Replace `<your_token_here>` with your actual token

        4. **Send the Request**:
        - Click "Send" to submit the GET request.
        - If successful, you'll receive a `200 OK` response with the approved evaluation request(s).

        5. **Handling Errors and Feedback**:
        - **404 Not Found**: If the `item_id` does not correspond to an existing item, you'll receive this status with an error message.
        - **No Approved Requests**: If no approved evaluation requests are found for the given `item_id`, you'll receive a feedback message indicating this.
        - **Multiple Approved Requests**: If there are more than one approved request for the same item, you'll get a warning message indicating a potential issue.
        """

        try:
            # Check if the item exists
            item = Item.objects.get(id=item_id)

            # Get all approved evaluation requests for the given item_id
            approved_requests = EvaluationRequest.objects.filter(item=item, status='approved')

            if not approved_requests:
                # If there are no approved requests, return a feedback message
                return Response(
                    {"message": "No approved evaluation requests found for this item."},
                    status=status.HTTP_200_OK
                )

            # Serialize the approved requests
            serializer = EvaluationRequestSerializer(approved_requests, many=True)

            # Check if there's more than one approved request
            if len(approved_requests) > 1:
                # If more than one approved request, return them with an error message
                return Response(
                    {
                        "error": "More than one approved evaluation request found for this item. Please investigate.",
                        "approved_requests": serializer.data,
                    },
                    status=status.HTTP_200_OK
                )

            # If only one approved request, return it
            return Response(
                {"approved_request": serializer.data[0]},
                status=status.HTTP_200_OK
            )

        except Item.DoesNotExist:
            # If the item doesn't exist, return a 404 with appropriate feedback
            return Response(
                {"error": f"Item with ID {item_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

# MUST RETURN EVALUATOR ID, FIX IT
# class SendItemevaluationRequestAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # Ensure the authenticated user is an evaluator
#         if not request.user.is_evaluator:
#             return Response(
#                 {"error": "Only evaluators can send evaluation requests."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         item_id = request.data.get("item_id")
#         message = request.data.get("message", "")

#         if not item_id:
#             return Response(
#                 {"error": "item_id is required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             item = Item.objects.get(id=item_id)
#         except ObjectDoesNotExist:
#             return Response(
#                 {"error": "Item not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         # Provide necessary data to the serializer
#         data = {
#             "item_id": item_id,  # Item primary key
#             "message": message,  # Optional message
#         }

#         # Use the serializer to validate and create the evaluation request
#         serializer = EvaluationRequestSerializer(data=data)

#         if serializer.is_valid():
#             # Save with the authenticated user as the evaluator
#             evaluation_request = serializer.save(
#                 item=item,
#                 evaluator=request.user,  # Manually set the evaluator to the authenticated user
#                 status="requested",  # Set the status to 'requested'
#             )

#             # Serialize the response to ensure the correct data is returned
#             response_serializer = EvaluationRequestSerializer(evaluation_request)

#             return Response(
#                 response_serializer.data,
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


