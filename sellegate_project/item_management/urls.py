from django.urls import path
from .views import ItemSearchAPIView, ItemDetailView, ItemListCreateAPIView, PurchaseItemAPIView


urlpatterns = [
    # Define URL patterns here
    path('search/', ItemSearchAPIView.as_view(), name='item-search'),
    path('<int:itemId>/', ItemDetailView.as_view(), name='item-detail'),
    path('list/', ItemListCreateAPIView.as_view(), name='item-list-create'),
    path('buy/', PurchaseItemAPIView.as_view(), name='buy_item'),
]