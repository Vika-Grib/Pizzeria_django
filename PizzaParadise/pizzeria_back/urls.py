from django.urls import path
from . import views

urlpatterns = [
 path('', views.basket, name='basket'),
 path('customer/add_to_cart', views.add_to_cart)
]