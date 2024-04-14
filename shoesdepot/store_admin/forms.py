from django import forms
from ..store.models import Product, Category
from ..common import form_mixins


class CreatProductForm(form_mixins.BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'is_on_sale', 'sale_price', 'sizes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()
        self.fields['is_on_sale'].widget.attrs['class'] = 'form-check-input'
        self.fields['sizes'].widget.attrs['class'] = 'form-select'
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['category'].queryset = Category.objects.filter(parent__isnull=False)
