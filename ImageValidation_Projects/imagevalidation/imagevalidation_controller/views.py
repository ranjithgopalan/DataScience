from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Image
from .serializer import ImageSerializer


# Create your views here.

class imageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


def main(request):
    return HttpResponse("Hello, world. You're at the imagevalidation main page.")