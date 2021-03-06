from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Slider
from pages.models import Page
from cart.forms import CartAddProductForm
from .recommender import Recommender

def home(request):
    sliders = Slider.objects.filter(active=True)
    # this Queryset is used in temporary home page
    temp_products = Product.objects.filter(temp_product=True)
    # Queryset for Pages
    pages = Page.objects.all().filter(active=True)
    return render(request,
                  'shop/product/temp_home.html',
                  {'sliders': sliders,
                   'products': temp_products,
                   'pages': pages})


def product_list(requset, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(requset,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})
