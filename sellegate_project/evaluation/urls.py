from django.urls import path
from . import views
from .views import DelegateItemAPIView, send_assessment_request

urlpatterns = [
    path('items/delegate/', DelegateItemAPIView.as_view(), name='delegate-item-to-evaluators'),
    path('evaluation/request', send_assessment_request.as_view(), name='send_assessment_request')
]