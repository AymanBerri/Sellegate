from django.urls import path
from .views import SearchItemsToEvaluateAPIView, ApprovedEvaluationRequestAPIView
from .views import (
    SendEvaluationRequestAPIView,
    GetMyEvaluationsAPIView, 
    GetEvaluationRequestsOnMyProductAPIView,
    RejectEvaluationAPIView,
    AcceptEvaluationAPIView)

urlpatterns = [

     # API endpoint for sending an assessment request
    path('new/', SendEvaluationRequestAPIView.as_view(), name='new-assessment'),

    # API endpoint to retrieve all assessments created by the current evaluator
    path('my/', GetMyEvaluationsAPIView.as_view(), name='my-assessments'),

    # API endpoint to retrieve all assessment requests for a specific item owned by the current user
    path('product/', GetEvaluationRequestsOnMyProductAPIView.as_view(), name='product-assessments'),

    # API endpoints for rejecting and accepting assessments
    path('<int:evaluation_id>/reject/', RejectEvaluationAPIView.as_view(), name='reject-assessment'),
    path('<int:evaluation_id>/accept/', AcceptEvaluationAPIView.as_view(), name='accept-assessment'),


    # OLD \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
    # Define URL patterns here
    path('items/', SearchItemsToEvaluateAPIView.as_view(), name='search-items-to-evaluate'),
    # path('request/', SendItemAssessmentRequestAPIView.as_view(), name='send-item-assessment-request'),

    # URL to get the approved evaluation request(s) for a given item_id
    path('approved-evaluation/<int:item_id>/', ApprovedEvaluationRequestAPIView.as_view(), name='approved-evaluation'),
]
