from django.shortcuts import render
from django.http import HttpResponse
from .models import Order


def main(request):
    # return HttpResponse('Это домашняя начальная страница!')
    return render(request, 'main.html')

# def home(request):
#     return render(request, 'home.html')

