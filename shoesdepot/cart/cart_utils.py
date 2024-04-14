from django.shortcuts import redirect
from ..store.models import Product


def _cart_summary(cart):
    cart_items = []
    total_price = 0.0
    for cart_key, item in cart.items():
        try:
            product = Product.objects.get(pk=item['product'])
            price = product.sale_price if product.is_on_sale else product.price
            item_total = price * item['quantity']
            total_price += float(item_total)
            cart_items.append({
                'cart_key': cart_key,
                'product': product,
                'quantity': item['quantity'],
                'size': item['size'],
                'item_total': item_total
            })
        except Product.DoesNotExist:
            pass
    return {'cart_items': cart_items, 'total_price': total_price}


def _update_cart(request, cart_key, delete=False):
    cart = request.session.get('cart', {})
    if delete and cart_key in cart:
        del cart[cart_key]

    elif request.POST.get('quantity') and cart_key in cart:
        quantity = int(request.POST.get('quantity'))
        cart[cart_key]['quantity'] = quantity

    cart_items_count = sum(item['quantity'] for item in cart.values())
    request.session['cart_items_count'] = cart_items_count
    request.session['cart'] = cart

    return redirect('cart_summary')


def _add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('size')
    cart = request.session.get('cart', {})
    cart_key = f"{product_id}_{size}"

    if cart_key in cart:
        cart[cart_key]['quantity'] += quantity
    else:
        cart[cart_key] = {
            'product': product_id,
            'size': size,
            'quantity': quantity,
        }

    request.session['cart'] = cart
    cart_items_count = sum(item['quantity'] for item in cart.values())
    request.session['cart_items_count'] = cart_items_count
    return {'cart_items_count': cart_items_count}
