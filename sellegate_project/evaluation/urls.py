from django.urls import path
from .views import SearchItemsToEvaluateAPIView, SendItemAssessmentRequestAPIView

urlpatterns = [
    # Define URL patterns here
    path('items/', SearchItemsToEvaluateAPIView.as_view(), name='search-items-to-evaluate'),
    path('request/', SendItemAssessmentRequestAPIView.as_view(), name='send-item-assessment-request'),

]