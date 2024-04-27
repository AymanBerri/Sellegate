# authentication/urls.py

from django.urls import path
from authentication.views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserDetailAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('user/<int:id>/', UserDetailAPIView.as_view(), name='user_detail'),  # New API endpoint

]