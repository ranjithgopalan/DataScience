
from django.contrib import admin
from django.urls import path,include

from .views import imageView

urlpatterns = [
    
    path('',imageView.as_view())
]