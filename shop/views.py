from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

from .models import Category, Product, Slider, Comment
from pages.models import Page
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .forms import SearchForm, CommentForm


def home(request):
    sliders = Slider.objects.filter(active=True)

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

    # list of active comments
    comments = product.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # Check wether user is logined or not
        if not request.user.is_authenticated:
            return redirect('login')

        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create comment object
            new_comment = comment_form.save(commit=False)

            #Assign the current product to the comments
            new_comment.product = product

            #Assign the current user to the comments
            new_comment.user = request.user

            # Save the comment
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Recommender engine
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    # Queryset for Pages
    pages = Page.objects.all().filter(active=True)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products,
                   'pages': pages,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form })


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
