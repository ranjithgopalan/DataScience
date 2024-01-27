
from django.contrib import admin
from django.urls import path,include

from .views import imageView

urlpatterns = [
    
    path('Image',imageView.as_view())
]