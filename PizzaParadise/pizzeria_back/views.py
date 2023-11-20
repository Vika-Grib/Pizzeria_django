import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .producer import send_message


def basket(request):
    cart = request.session.get('cart', [])
    return render(request, 'basket.html', {'cart': cart})

@csrf_exempt
def add_to_cart(request, *args):
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
        send_message(order_data)
    return HttpResponse('''<html><script>window.location.replace('/customer');</script></html>''')
    # чтобы мы переадресовывались на ту же страницу
        