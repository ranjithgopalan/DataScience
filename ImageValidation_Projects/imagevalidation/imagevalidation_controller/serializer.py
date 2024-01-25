from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'imagename','imagesize' 'uploaded_at', 'user', 'created_at')
    
