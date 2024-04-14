from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.urls import reverse_lazy
from ..store.models import Product
from .forms import CreatProductForm


class ModeratorRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.profile.is_moderator:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class ProductCreateView(ModeratorRequiredMixin, CreateView):
    model = Product
    form_class = CreatProductForm
    template_name = 'store_admin/products_create.html'
    success_url = reverse_lazy('admin_products_list')


class ProductUpdateView(ModeratorRequiredMixin, UpdateView):
    model = Product
    form_class = CreatProductForm
    template_name = 'store_admin/products_edit.html'
    success_url = reverse_lazy('admin_products_list')


class ProductDeleteView(ModeratorRequiredMixin, DeleteView):
    model = Product
    template_name = 'store_admin/products_delete.html'
    success_url = reverse_lazy('admin_products_list')


class ProductListView(ModeratorRequiredMixin, ListView):
    model = Product
    template_name = 'store_admin/admin_products_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {}

        if self.request.GET.get('pk'):
            filters['pk'] = self.request.GET.get('pk')
        if self.request.GET.get('category'):
            filters['category__pk'] = self.request.GET.get('category')
        if self.request.GET.get('search_query'):
            filters['search_query'] = self.request.GET.get('search_query')

        if filters:
            queryset = queryset.filter(**filters)

        return queryset
