from django.template.defaulttags import url
from django.urls import path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
 path('', views.basket, name='basket'),
 path('customer/add_to_cart', views.add_to_cart),
 path('customer/order_info', views.info_for_user),
 # url(r'customer/order_info/(?P<order_id>\w{1,10})', views.info_for_user)
]