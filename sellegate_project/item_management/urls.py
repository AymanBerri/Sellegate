from django.urls import path
from .views import ItemSearchAPIView, ItemDetailView


urlpatterns = [
    # Define URL patterns here
    path('search/', ItemSearchAPIView.as_view(), name='item-search'),
    path('<int:itemId>/', ItemDetailView.as_view(), name='item-detail'),
]