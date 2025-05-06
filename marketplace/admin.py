from django.contrib import admin
from .models import Restaurant, Categories, FoodItem, CartItem, Order, OrderItem, Review, Payment, Notification


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'phonenumber', 'created_at','image')
    search_fields = ('name', 'owner__username', 'address')


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('restaurant',)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'categories', 'price', 'available', 'created_at')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('restaurant', 'available', 'categories')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditems', 'quantity', 'added_at')
    search_fields = ('user__username', 'fooditems__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'total_price', 'delivery_address', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('status', 'restaurant', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'food_item', 'quantity', 'price')
    search_fields = ('order__id', 'food_item__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'created_at')
    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('rating',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'reference', 'verify', 'date_created')
    search_fields = ('user__username', 'order__id', 'refrence')
    list_filter = ('verify', 'date_created')
    
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("name", "message", "has_read", "created_at")
    list_filter = ("created_at", "has_read")
    search_fields = ("name", "message")