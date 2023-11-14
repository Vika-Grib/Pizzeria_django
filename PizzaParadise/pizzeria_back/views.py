from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def basket(request):
    cart = request.session.get('cart', [])
    return render(request, 'basket.html', {'cart': cart})

def add_to_cart(request, product_id):
    try:
        product_id = int(product_id)
        # Добавляем товар в корзину
        cart = request.session.get('cart', {})
        cart_item = cart.get(product_id, {'quantity': 0})
        cart_item['quantity'] += 1
        cart[product_id] = cart_item
        request.session['cart'] = cart

        return JsonResponse({'message': f'Товар с id {product_id} добавлен в корзину!'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
