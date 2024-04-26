"""
URL configuration for sellegate_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('evaluator/', include('evaluator.urls')),
    path('api/evaluation/', include('evaluation.urls')),

    path('cart/', include('cart.urls')),
    path('rating_management/', include('rating_management.urls')),
    
    path('items/', include('item_management.urls')),

    path('auth/', include('authentication.urls')), # this path is for the authentication urls, they all are prefixed with "auth/"
    # Add more app URLs as needed
]