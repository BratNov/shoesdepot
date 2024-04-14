from random import sample
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView
from ..app_auth.forms import ProfileForm
from ..app_auth.models import Profile
from ..store.models import Product, Size
from ..orders.models import Order, OrderItem, OrderAddress
from .cart_utils import _cart_summary, _update_cart, _add_to_cart


def cart_add_view(request):
    return JsonResponse(_add_to_cart(request))


def cart_summary_view(request):
    cart = request.session.get('cart', {})
    context = _cart_summary(cart)
    context['products'] = sample(list(Product.objects.all()), 8)
    return render(request, 'cart/cart_summary.html', context)


@require_POST
def cart_update_view(request, cart_key):
    return _update_cart(request, cart_key)


def cart_delete_view(request, cart_key):
    return _update_cart(request, cart_key, delete=True)


class CartCheckoutView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'cart/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        context.update(_cart_summary(cart))
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        profile = form.instance
        profile.save()
        order = self.create_order(profile)
        self.create_order_items(order)
        self.create_order_address(order, profile)
        self.clear_session_data()
        return redirect('order_detail', pk=order.pk)

    def create_order(self, profile):
        return Order.objects.create(user=self.request.user)

    def create_order_items(self, order):
        cart = self.request.session.get('cart', {})
        for cart_item_data in cart.values():
            product_id = cart_item_data['product']
            quantity = cart_item_data['quantity']
            size_name = cart_item_data['size']

            product = Product.objects.get(pk=product_id)
            size = Size.objects.get(name=size_name)
            price = product.sale_price if product.is_on_sale else product.price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, size=size, price=price)

    def create_order_address(self, order, profile):
        address_data = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'phone_number': profile.phone_number,
            'address': profile.address,
            'country': profile.country,
            'city': profile.city,
            'postcode': profile.postcode
        }
        OrderAddress.objects.create(order=order, **address_data)

    def clear_session_data(self):
        del self.request.session['cart']
        del self.request.session['cart_items_count']
