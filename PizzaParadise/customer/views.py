from django.shortcuts import render
from django.views.generic import ListView
from .models import Order


class Orders_view(ListView):
    model = Order
    template_name = 'back.html'
    context_object_name = 'products'


def back_html(request):
    # return HttpResponse('Это домашняя начальная страница!')
    return render(request, 'back.html')

