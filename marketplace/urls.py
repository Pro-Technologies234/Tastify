from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/',views.restaurants_list, name='restaurants_list'),
    path("restaurants/<int:pk>/", views.restaurant_detail, name='restaurant_detail'),
    path("cart/", views.cart, name='cart'),
    path("food_items/<int:pk>/", views.fooditem_detail, name='fooditem_detail'),
    path("cart/add/<int:fooditems_id>/", views.add_to_cart, name='add_to_cart'),
    path("cart/remove/<int:cartitem_id>/", views.remove_cart_item, name='remove_cart_item'),
    path("quantity/add/<int:cartitem_id>/", views.add_quantity, name='add_quantity'),
    path("quantity/minus/<int:cartitem_id>/", views.minus_quantity, name='minus_quantity'),
    path("order/payment-method/", views.payment_method, name="payment_method" ),
    path("order/place/paystack", views.place_paystack_order, name='place_paystack_order'),
    path("order/place/flutterwave", views.place_flutterwave_order, name='place_flutterwave_order'),
    path("verify_paystack_payment/", views.verify_paystack_payment, name='verify_paystack_payment'),
    path("verify_flutterwave_payment/", views.verify_flutterwave_payment, name='verify_flutterwave_payment'),
    path('order-success/', views.order_success_page, name='order_success_page'),
    path("notification/mark_as_read/<int:notification_id>/", views.mark_as_read, name='mark_as_read'),
    # path("cart/view/", views.view_cart, name='view_cart'),
]
