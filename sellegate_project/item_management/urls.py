from django.urls import path
from .views import ItemSearchAPIView, ItemDetailView, ItemListCreateAPIView, PurchaseItemAPIView, UserPurchasesAPIView, UserSoldItemsAPIView, DeleteItemAPIView, UpdateItemAPIView
from .views import GetAllItemsAPIView, GetItemsToExploreAPIView, GetItemAPIView, UserProductsAPIView, PostItemAPIView

urlpatterns = [
    # Define URL patterns here
    # Get all items
    path('', GetAllItemsAPIView.as_view(), name='get-all-items'),  

    # retrieves items for the "Explore" feature while excluding those owned by the current user
    path('explore/', GetItemsToExploreAPIView.as_view(), name='get-items-to-explore'),  # New endpoint

    # Endpoint to get a specific item by its ID
    path('<int:id>/', GetItemAPIView.as_view(), name='get-item-by-id'),  # URL for the new endpoint

    # API endpoint to return all items owned by the currently logged-in user.
    path('user-products/', UserProductsAPIView.as_view(), name='get-user-products'),  # URL for user-specific products

    # API endpoint to create a new item.
    path('post-item/', PostItemAPIView.as_view(), name='post-item'),  # URL for posting a new item

    # API endpoint to update an item.
    path('update-item/<int:item_id>/', UpdateItemAPIView.as_view(), name='update-item'),  # Endpoint for updating an item

    # API endpoint to delete an item based on its ID.
    path('delete-item/<int:item_id>/', DeleteItemAPIView.as_view(), name='delete-item'),

    # OLD \/\/\/\/\/\/

    # Get all items (This is better as it handles extra queries)
    path('search/', ItemSearchAPIView.as_view(), name='item-search'), # Replaced by ''

    # Endpoint to get a specific item by its ID
    path('<int:item_id>/', ItemDetailView.as_view(), name='item-detail'), # Replaced by '<int:id>/'

    path('list/', ItemListCreateAPIView.as_view(), name='item-list-create'), #to create a new item

    path('buy/', PurchaseItemAPIView.as_view(), name='buy_item'),

    # URL for fetching all purchases made by the authenticated user
    path('my-purchases/', UserPurchasesAPIView.as_view(), name='user-purchases'),

    # URL for fetching all items sold by the authenticated user
    path('my-sold-items/', UserSoldItemsAPIView.as_view(), name='user-sold-items'),

    # URL for updating an item by its ID
    # path('update-item/<int:item_id>/', UpdateItemAPIView.as_view(), name='update-item'), 

    # URL for deleting an item by its ID
    path('delete-item/<int:item_id>/', DeleteItemAPIView.as_view(), name='delete-item'),
]
