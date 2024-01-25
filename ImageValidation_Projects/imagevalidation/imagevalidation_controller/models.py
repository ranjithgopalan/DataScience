from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    imagename = models.CharField(max_length=100, default='')
    imagesize = models.IntegerField(default=0)
    # imageSize = models.CharField(max_length=100, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    