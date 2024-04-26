# In evaluation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('evaluators/<int:evaluator_id>/earnings', views.view_earnings, name='view_earnings'),
    path('evaluators/<int:evaluator_id>', views.update_profile, name='update_profile'),
]
