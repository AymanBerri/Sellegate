from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from item_management.models import Item  # Import Item model from item_management app
from item_management.serializers import ItemSerializer  # Import ItemSerializer from item_management app
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

@require_POST
def DelegateItemAPIView(request):
    # Extract data from request body
    item_id = request.POST.get('item_id')
    user_id = request.POST.get('user_id')  # Assuming the user ID is sent with the request
    
    # Check if item exists
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
    # Check if the user is the owner of the item (seller)
    if item.seller_id != user_id:
        return JsonResponse({'error': 'You are not authorized to delegate this item'}, status=403)
    
    # Perform delegation logic (update item's delegation state)
    item.delegation_state = 'pending_evaluation'
    item.save()
    
    # Return success response
    return JsonResponse({'success': True})

@api_view(['GET'])
def search_items_to_evaluate(request):
    if request.method == 'GET':
        status = request.query_params.get('status', 'Pending')
        items = Item.objects.filter(delegation_state=status)
        serializer = ItemSerializer(items, many=True)
        return Response({'items': serializer.data})

@api_view(['POST'])
def send_assessment_request(request):
    if request.method == 'POST':
        serializer = AssessmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve data from serializer
            item_id = serializer.validated_data['itemId']
            evaluator_id = serializer.validated_data['evaluatorId']
            message = serializer.validated_data['message']
            
            # Check if the item exists
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                return Response({'error': 'Item not found'}, status=404)
            
            # Perform logic to send assessment request
            # For example:
            # Send assessment request to evaluator_id for the item with message
            
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=400)