from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Product_pizza

class Products_view(ListView):
    model = Product_pizza
    template_name = 'menu.html'
    context_object_name = 'products'


def main(request):
    # return HttpResponse('Это домашняя начальная страница!')
    return render(request, 'menu.html')




