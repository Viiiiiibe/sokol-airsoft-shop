from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart-view'),
    path('add/', views.cart_add, name='add-to-cart'),
    path('delete/', views.cart_delete, name='delete-to-cart'),
    path('update/', views.cart_update, name='update-to-cart'),
    path('order/', views.order_view, name='order-view'),
    path('order/<int:number>/completed/', views.order_completed, name='order-completed'),
    path('delivery_order/', views.delivery_order_view, name='delivery-order-view'),
    path('delivery_order/<int:number>/completed/', views.delivery_order_completed,
         name='delivery-order-completed'),

]
