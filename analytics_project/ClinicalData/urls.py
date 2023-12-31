from django.urls import path
from . import views

urlpatterns = [
    path('', views.getclinicalData, name='getclinicalData'),



]