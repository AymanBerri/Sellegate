from django.urls import path
from .views import ItemSearchAPIView, ItemDetailView, ItemListCreateAPIView, PurchaseItemAPIView, UserPurchasesAPIView, UserSoldItemsAPIView, DeleteItemAPIView


urlpatterns = [
    # Define URL patterns here
    path('search/', ItemSearchAPIView.as_view(), name='item-search'),
    path('<int:item_id>/', ItemDetailView.as_view(), name='item-detail'),
    path('list/', ItemListCreateAPIView.as_view(), name='item-list-create'),
    path('buy/', PurchaseItemAPIView.as_view(), name='buy_item'),

    # URL for fetching all purchases made by the authenticated user
    path('my-purchases/', UserPurchasesAPIView.as_view(), name='user-purchases'),

    # URL for fetching all items sold by the authenticated user
    path('my-sold-items/', UserSoldItemsAPIView.as_view(), name='user-sold-items'),

    # URL for deleting an item by its ID
    path('delete-item/<int:item_id>/', DeleteItemAPIView.as_view(), name='delete-item'),
]
