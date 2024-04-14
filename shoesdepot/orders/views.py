from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Order, OrderItem, OrderAddress
from .forms import OrderStatusForm


class OrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.profile.is_moderator:
            queryset = queryset.filter(user=user)

        sort_by = self.request.GET.get('sort', 'newest')
        queryset = self.sort_orders(queryset, sort_by)

        return queryset

    def sort_orders(self, queryset, sort_by):
        if sort_by == 'oldest':
            return queryset.order_by('date_ordered')
        elif sort_by in dict(Order.STATUS_CHOICES).keys():
            return queryset.filter(status=sort_by)
        return queryset.order_by('-date_ordered')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', 'newest')
        context['sort_options'] = Order.STATUS_CHOICES + [('newest', 'Newest First'), ('oldest', 'Oldest First')]
        return context


class OrderDetailView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderStatusForm
    template_name = 'orders/order_detail.html'

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        user = self.request.user
        if not user.profile.is_moderator:
            return get_object_or_404(Order, pk=pk, user=user)
        return get_object_or_404(Order, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        order_items = OrderItem.objects.filter(order=order)
        order_address = OrderAddress.objects.get(order=order)
        context['order_items'] = order_items
        context['order_address'] = order_address
        return context
