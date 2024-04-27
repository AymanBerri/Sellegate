from django.urls import path
from .views import SearchItemsToEvaluateAPIView

urlpatterns = [
    # Define URL patterns here
    path('items/', SearchItemsToEvaluateAPIView.as_view(), name='search-items-to-evaluate'),
]