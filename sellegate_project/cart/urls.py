from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddToCartAPIView.as_view(), name='add_to_cart'),
    path('remove/', views.RemoveFromCartAPIView.as_view(), name='remove_from_cart'),
]