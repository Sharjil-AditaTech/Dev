from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.image_upload, name = 'upload'),    
]
