# In evaluation/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Evaluator
from .serializers import EarningsSerializer, EvaluatorProfileSerializer

@api_view(['GET'])
def view_earnings(request, evaluator_id):
    if request.method == 'GET':
        try:
            evaluator = Evaluator.objects.get(id=evaluator_id)
        except Evaluator.DoesNotExist:
            return Response({'error': 'Evaluator not found'}, status=404)
        
        serializer = EarningsSerializer(evaluator)
        return Response(serializer.data)

@api_view(['PATCH'])
def update_profile(request, evaluator_id):
    if request.method == 'PATCH':
        try:
            evaluator = Evaluator.objects.get(id=evaluator_id)
        except Evaluator.DoesNotExist:
            return Response({'error': 'Evaluator not found'}, status=404)
        
        serializer = EvaluatorProfileSerializer(evaluator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
