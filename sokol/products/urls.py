from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('all_products/', views.all_products, name='all_products'),
    path('categories/', views.categories, name='categories'),
    path('categories/subcategories/<slug:slug>', views.subcategories, name='subcategories'),
    path('categories/<slug:slug>/', views.category_products, name='category_products'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
]
