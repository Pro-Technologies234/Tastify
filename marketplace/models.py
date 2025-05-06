from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
User = settings.AUTH_USER_MODEL



# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='restaurant/', blank=True, null=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name','restaurant')
    
    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='fooditem/')
    available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name='fooditems')
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE, related_name='fooditems')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.restaurant}'
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartitem')
    fooditems = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='cartitem')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','fooditems')

    def __str__(self):
        return f'{self.quantity} x {self.fooditems.name} {self.user}'
    
    def add_quantity(self):
        self.quantity += 1
        return self.quantity
    
    def minus_quantity(self):
        self.quantity -= 1
        return self.quantity
    
    def get_total_price(self):
        return self.fooditems.price * self.quantity
    
    
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('preparing', 'Preparing'),
        ('on_the_way', 'On the Way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.CharField(max_length=255)

    class Meta:
        ordering = ['created_at']

    def _str_(self):
        return f"Order #{self.id} by {self.user}"

    def calculate_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def _str_(self):
        return f"{self.quantity} x {self.food_item.name} (Order #{self.order.id})"

    def get_total_price(self):
        return self.price * self.quantity


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # Could be 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def _str_(self):
        return f"{self.user} rated {self.restaurant} - {self.rating}/5"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment")
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    verify = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payement for #{self.order.id} by {self.user.name}"


class Notification(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField(max_length=255)
    image = models.ImageField(upload_to="notifications/image")
    has_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# 🚨 SIGNAL: Remove cart items after order is placed
@receiver(post_save, sender=Order)
def clear_cart_after_order(sender, instance, created, **kwargs):
    if created:
        CartItem.objects.filter(user=instance.user).delete()