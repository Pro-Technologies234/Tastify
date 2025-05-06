from django.db import models

# Create your models here.
class FoodShowcase(models.Model):
    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(max_length=255, blank=True)
    image_1 = models.ImageField(upload_to="foodshowcase/")
    image_2 = models.ImageField(upload_to="foodshowcase2/")
    image_3 = models.ImageField(upload_to="foodshowcase3/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)