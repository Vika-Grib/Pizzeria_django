import sqlite3

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Product_pizza

# class Products_view(ListView):
#     model = Product_pizza
#     template_name = 'menu.html'
#     context_object_name = 'products'


def main(request):
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * from Snacks''')
    snacks = list(cursor.fetchall())
    data = []
    for snack in snacks:
        data.append({'id': snack[0], 'title': snack[1], 'big_price': snack[2], 'short_description': snack[3], 'photo': snack[4]})
    # return HttpResponse('Это домашняя начальная страница!')
    print(data, 'DATA!!!!')
    cursor.execute(f'''SELECT * from Menu_product_pizza''')
    pizzas = list(cursor.fetchall())
    products = []
    for pizza in pizzas:
        products.append({'id': pizza[0], 'title': pizza[1], 'big_price': pizza[2], 'medium_price': pizza[3], 'thin_price': pizza[4], 'ingredients': pizza[5],
                     'image': pizza[6]})

    return render(request, 'menu.html', {'snacks': data, 'products': products})




