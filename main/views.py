from django.shortcuts import render, redirect
from . models import FoodShowcase

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return redirect('restaurants_list')
    food_showcase = FoodShowcase.objects.filter(is_active=True)
    return render(request,'main/home.html', 
                  {
                      "food_showcase" : food_showcase
                }
                  )