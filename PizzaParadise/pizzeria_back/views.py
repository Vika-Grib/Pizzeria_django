import json
import sqlite3

from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User_order
from .producer import send_message


def basket(request):
    cart = request.session.get('cart', [])
    return render(request, 'basket.html', {'cart': cart})


def info_for_user(request):
    print(request.GET.get('order_id'))
    order_id = request.GET.get('order_id')
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * from pizzeria_back_user_order WHERE order_id="{order_id}"''')
    order = list(cursor.fetchall())[0]
    order = {'order_id': order[1], 'status': order[2]}
    print(order, '******************')
    return render(request, 'info_for_user.html', {'order': order})  # это мы его подгружаем {% if order %}

class Orders_view(ListView):
    model = User_order
    template_name = 'info_for_user.html'
    context_object_name = 'order'

@csrf_exempt
def add_to_cart(request, *args):
    order_id = 0
    if request.method == 'POST':   # наша формочка выполняет запрос POST, тут мы её отлавливаем
        pizza_data = request.POST.get("hidden_data")
        payment = request.POST.get("payment")
        address = request.POST.get("address")
        mail = request.POST.get("mail")
        pizza_data = str(pizza_data[1:-1]).split('},{')
        pizza_list = []
        order_id = 0
        for pizza in pizza_data:
            pizza = '{' + pizza + '}'
            pizza = json.loads(pizza)
            print(pizza)
            order_id = pizza['order_id']
            pizza_list.append(pizza)
        order_data = {'order_id': order_id, 'payment': payment, 'address': address, 'mail': mail, 'pizza': pizza_list}
        conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f'''INSERT INTO pizzeria_back_user_order(order_id, status) VALUES (?,?)''', (order_id, 'Принят'))
        conn.commit()
        send_message(order_data)
    return HttpResponse(f'''<html><script>window.location.replace('/customer/customer/order_info?order_id={order_id}');</script></html>''')
    # чтобы мы переадресовывались на ту же страницу
        