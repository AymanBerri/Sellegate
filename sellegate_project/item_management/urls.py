from django.urls import path
from .views import ItemSearchAPIView


urlpatterns = [
    # Define URL patterns here
    path('search/', ItemSearchAPIView.as_view(), name='item-search'),
]