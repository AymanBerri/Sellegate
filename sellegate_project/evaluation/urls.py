from django.urls import path
from .views import SearchItemsToEvaluateAPIView, ApprovedEvaluationRequestAPIView
from .views import (
    SendEvaluationRequestAPIView,
    GetMyEvaluationsAPIView, 
    GetEvaluationRequestsOnMyProductAPIView,
    RejectEvaluationAPIView,
    AcceptEvaluationAPIView)

urlpatterns = [

     # API endpoint for sending an evaluation request
    path('new/', SendEvaluationRequestAPIView.as_view(), name='new-evaluation'),

    # API endpoint to retrieve all evaluations created by the current evaluator
    path('my/', GetMyEvaluationsAPIView.as_view(), name='my-evaluations'),

    # API endpoint to retrieve all evaluation requests for a specific item owned by the current user
    path('product/', GetEvaluationRequestsOnMyProductAPIView.as_view(), name='product-evaluations'),

    # API endpoints for rejecting and accepting evaluations
    path('<int:evaluation_id>/reject/', RejectEvaluationAPIView.as_view(), name='reject-evaluation'),
    path('<int:evaluation_id>/accept/', AcceptEvaluationAPIView.as_view(), name='accept-evaluation'),


    # OLD \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
    # Define URL patterns here
    path('items/', SearchItemsToEvaluateAPIView.as_view(), name='search-items-to-evaluate'),
    # path('request/', SendItemevaluationRequestAPIView.as_view(), name='send-item-evaluation-request'),

    # URL to get the approved evaluation request(s) for a given item_id
    path('approved-evaluation/<int:item_id>/', ApprovedEvaluationRequestAPIView.as_view(), name='approved-evaluation'),
]
