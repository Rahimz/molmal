from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

from .models import Category, Product, Slider
from pages.models import Page
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .forms import SearchForm

def home(request):
    sliders = Slider.objects.filter(active=True)
    # this Queryset is used in temporary home page
    # temp_products = Product.objects.filter(temp_product=True)

    products = Product.objects.filter(available=True)[:10]
    # Queryset for Pages
    pages = Page.objects.all().filter(active=True)

    form = SearchForm()
    return render(request,
                  'shop/product/home.html',
                  {'sliders': sliders,
                   'products': products,
                   'pages': pages,
                   'form': form})


@staff_member_required
def price_view(request,):
    categories = Category.objects.all()
    products = Product.objects.filter(Q(available=True) & Q(stock__gte=1)).order_by('category')
    return render(request,
                  'shop/product/price_list.html',
                  {'products': products,
                   'categories': categories, })


def product_list(requset, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # Queryset for Pages
    pages = Page.objects.all().filter(active=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    form = SearchForm()
    return render(requset,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'form':form,
                   'pages': pages})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    # Queryset for Pages
    pages = Page.objects.all().filter(active=True)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products,
                   'pages': pages})


def product_search(request):
    form = SearchForm()
    query = None
    results = []

    # Queryset for Pages
    pages = Page.objects.all().filter(active=True)

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.all().annotate(
                search=SearchVector('name', 'short_description'),
            ).filter(search=query)
    return render(request,
                  'shop/product/search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'pages': pages})
