from django.contrib import admin
from .models import FoodShowcase
# Register your models here.
@admin.register(FoodShowcase)
class FoodShowcaseAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")