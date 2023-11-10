from django.urls import path
from . import views

urlpatterns = [
 path('', views.back_customer, name='back_customer'),
]