from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('our_team/', views.our_team, name='our_team'),
    path('contacts/', views.contacts, name='contacts'),
    path('payment_and_delivery/', views.payment_and_delivery, name='payment_and_delivery'),
]
