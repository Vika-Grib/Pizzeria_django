from django.urls import path
from . import views
from .views import Orders_view

urlpatterns = [
 path('', Orders_view.as_view(), name="back"),
]