from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator
from django.db.models import Case, When, Q


def home(request):
    search_query = request.GET.get('search_query')

    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    else:
        products = list(Product.objects.all().order_by('?')[:8])
    return render(request, 'store/home.html', {'products': products})


def product_details(request, slug):
    product_info = get_object_or_404(Product, slug=slug)
    category_products = Product.objects.filter(category=product_info.category)

    if category_products.count() < 8:
        products = list(category_products.order_by('?'))
        other_category_products = Product.objects.exclude(category=product_info.category)
        products.extend(other_category_products.order_by('?')[:8 - len(products)])
    else:
        products = list(category_products.order_by('?')[:8])

    context = {
        'product': product_info,
        'main_category': product_info.category.parent,
        'products': products
    }
    return render(request, 'store/product_details.html', context)


def category_details(request, category_slug, subcategory_slug):
    main_category = get_object_or_404(Category, slug=category_slug)
    subcategory = None

    if subcategory_slug == 'all':
        subcategories = Category.objects.filter(parent=main_category)
        products = Product.objects.filter(category__in=subcategories)
    else:
        subcategory = get_object_or_404(Category, slug=subcategory_slug)
        products = Product.objects.filter(category=subcategory)

    price_sort = Case(When(is_on_sale=True, then='sale_price'), default='price')
    SORT_OPTIONS = {
        'price_low_to_high': price_sort,
        'price_high_to_low': price_sort.desc(),
        'name': 'name',
        'oldest_first': 'id',
        'newest_first': '-id',
    }

    default = SORT_OPTIONS['newest_first']
    sort_by = request.GET.get('sort')
    sorting_key = SORT_OPTIONS.get(sort_by, default)
    products = products.order_by(sorting_key)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'subcategory': subcategory,
        'main_category': main_category,
        'sort_options': {k: k.replace('_', ' ').title() for k in SORT_OPTIONS}
    }
    return render(request, 'store/categories.html', context=context)
