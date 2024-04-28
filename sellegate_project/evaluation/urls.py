from django.urls import path
from .views import SearchItemsToEvaluateAPIView, SendItemAssessmentRequestAPIView, ApprovedEvaluationRequestAPIView

urlpatterns = [
    # Define URL patterns here
    path('items/', SearchItemsToEvaluateAPIView.as_view(), name='search-items-to-evaluate'),
    path('request/', SendItemAssessmentRequestAPIView.as_view(), name='send-item-assessment-request'),

    # URL to get the approved evaluation request(s) for a given item_id
    path('approved-evaluation/<int:item_id>/', ApprovedEvaluationRequestAPIView.as_view(), name='approved-evaluation'),
]
