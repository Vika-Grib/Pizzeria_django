from django.urls import path
from django.views.generic import ListView
from . import views
from .models import Product_pizza
# from .views import Products_view


urlpatterns = [
 # path('', Products_view.as_view(), name="menu"),
 path('', views.main, name='menu')
]