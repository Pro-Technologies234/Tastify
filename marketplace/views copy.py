from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Restaurant, FoodItem, CartItem, Order, OrderItem, Payment, Review
from django.conf import settings
import uuid
import requests


@login_required
def restaurants_list(request):
    restaurants = Restaurant.objects.all()
    cart_item = CartItem.objects.filter(user = request.user)
    total_cart_item = sum(item.quantity for item in cart_item)
    return render(request, 'marketplace/restaurant/list.html', {'restaurants': restaurants, 'total_cart_item': total_cart_item,} )

@login_required
def restaurant_detail(request, pk):
    restaurants = get_object_or_404(Restaurant, pk=pk)
    categories = restaurants.categories.filter()
    food_items = restaurants.fooditems.filter(available = True)
    # cart_amount = CartItem.objects.filter(user = request.user)
    cart_item = CartItem.objects.filter(user = request.user)
    total_cart_item = sum(item.quantity for item in cart_item)
    total = sum(item.get_total_price()  for item in cart_item)
    
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")
        review = Review.objects.update_or_create(
            user=request.user,
            restaurant=restaurants,
            defaults={
                "rating": rating,
                "comment": comment,
                "created_at": timezone.now()
            }
        )
        messages.success(request,"Thank you for your Feedback")
        return redirect("restaurant_detail",pk=pk)
    return render(request, 'marketplace/restaurant/details.html', 
                  {
                      'restaurants': restaurants,
                      'categories' : categories,
                      'food_items': food_items,
                      'total_cart_item': total_cart_item,
                      'total': total
                })
    
@login_required
def cart(request):
    # cart_amount = CartItem.objects.filter(user = request.user)
    cart_item = CartItem.objects.filter(user = request.user)
    total_cart_item = sum(item.quantity for item in cart_item)
    total = sum(item.get_total_price()  for item in cart_item)
    return render(request, 'marketplace/restaurant/cart.html', 
                  {
                      'cart_item': cart_item,
                      'total_cart_item': total_cart_item,
                      'total': total
                })

@login_required
def add_to_cart(request,fooditems_id):
    food_items = get_object_or_404(FoodItem, pk=fooditems_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, fooditems=food_items)
    if not created:
        cart_item.quantity +=1;
    cart_item.save()
    messages.success(request, f'{food_items.name } Added to cart Success')
    return redirect('restaurant_detail', pk=food_items.restaurant.pk)
  

def fooditem_detail(request, pk):
    food_items = get_object_or_404(FoodItem, pk=pk)
    return render(request, 'marketplace/restaurant/food_details.html', {'food_items': food_items})

@login_required
def remove_cart_item(request,cartitem_id):
    cart_item = get_object_or_404(CartItem,user = request.user, pk=cartitem_id)
    cart_item.delete()
    messages.success(request, f'! {cart_item.fooditems.name } Removed from cart Succesfully')
    return redirect('cart')  

@login_required
def add_quantity(request,cartitem_id):
    cart_item = get_object_or_404(CartItem, user = request.user, pk = cartitem_id)
    cart_item.add_quantity()
    cart_item.save()
    messages.success(request, f'1 {cart_item.fooditems.name } Added to cart Succesfully')
    return redirect('cart')  

@login_required
def minus_quantity(request,cartitem_id):
    cart_item = get_object_or_404(CartItem, user = request.user, pk = cartitem_id)
    if cart_item.quantity > 1:
        cart_item.minus_quantity()
        cart_item.save()
        messages.success(request, f'1 {cart_item.fooditems.name } Removed from cart Succesfully')
    else :
        remove_cart_item(request,cartitem_id)
        messages.success(request, f'! {cart_item.fooditems.name } Removed from cart Succesfully')
    return redirect('cart')  


@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('restaurants_list')

    if request.method == "POST":
        address = request.POST.get("address")
        if not address:
            messages.error(request, "Delivery address is required.")
            return redirect('place_order')
        try:
            # Debugging cart items
            print(f"[DEBUG] Found {cart_items.count()} cart item(s) for user {request.user}.")

            # Get restaurant from first cart item
            restaurant = cart_items[0].fooditems.restaurant

            total = sum(item.fooditems.price * item.quantity for item in cart_items)
            # Create order first
            order = Order.objects.create(
                user=request.user,
                restaurant=restaurant,
                delivery_address=address,
                total_price = total
            )
            print(f"[DEBUG] Created Order #{order.id}.")


            for item in cart_items:
                try:
                    
                    # item_total = item.quantity * total
                    # total = item_total

                    # Debug output for item being processed
                    print(f"[DEBUG] Creating OrderItem for {item.fooditems.name} (x{item.quantity})")

                    OrderItem.objects.create(
                        order=order,
                        food_item=item.fooditems,
                        quantity=item.quantity,
                        price=item.fooditems.price
                    )
                except Exception as item_err:
                    print(f"[ERROR] Failed to create OrderItem for {item.fooditems.name}: {item_err}")
                    messages.error(request, f"Could not add {item.fooditems.name} to order.")
                    # Optionally: rollback or skip to next

            # Set total and save
            order.total_price = total
            order.save(update_fields=["total_price"])
            print(f"[DEBUG] Order #{order.id} total price set to {total}.")

            # Optional: clear cart (if signal isn't doing it)
            cart_items.delete()
            print("[DEBUG] Cart items cleared.")

            reference = str(uuid.uuid4())
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=total,
                reference=reference,
            )
            
            paystack_secret_key = settings.PAYSTACK_SECRET_KEY
            headers = {
                "Authorization" : f"Bearer {paystack_secret_key}",
                "Content-Type" : "application/json"
            }
            
            callback_url = request.build_absolute_uri("/verify_payment/")
            data = {
                "email" : request.user.email,
                "amount" : int(total * 100),
                "reference" : reference,
                "callback_url" : callback_url,
            }
            
            response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get('status'):
                return redirect(response_data['data']['authorization_url'])
            else:
                messages.error(request, "Payement Authorization Failed")
                return redirect('place_order')


        except Exception as e:
            print(f"[ERROR] Failed to place order: {e}")
            messages.error(request, "Some thing went wrong while placing your order. Please try again.")

    return render(request, 'marketplace/order/place_order.html', {'cart_items': cart_items})



@login_required
@csrf_exempt
def verify_payment(request):
    reference = request.GET.get('reference')

    try:
        payment = Payment.objects.get(reference=reference)

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        response_data = response.json()
        print(response_data)
        if response_data['data']['status'] == 'success':
            payment.verified = True
            payment.save()
            print(payment.verified)
            messages.success(request, f"Payment for Order #{payment.order.id} was successful.")
            return redirect('order_success_page')  # create this URL/view
        else:
            messages.error(request, "Payment verification failed.")
            return redirect('place_order')

    except Payment.DoesNotExist:
        messages.error(request, "Invalid payment reference.")
        return redirect('place_order')
    return render(request, 'marketplace/order/verify_payement.html')


@login_required
def order_success_page(request):
    return render(request, 'marketplace/order/order_success.html')

    
