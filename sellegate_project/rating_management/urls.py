from django.urls import path
from .views import rate_evaluator, rate_seller

urlpatterns = [
    path('ratings/evaluator/', rate_evaluator, name='rate_evaluator'),
    path('ratings/seller/', rate_seller, name='rate_seller'),
]
