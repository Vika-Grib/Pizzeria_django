from django.http import HttpResponse
from django.shortcuts import render


def back_customer(request):
    return HttpResponse('Это страница!')
    #return render(request, 'basket.html')
