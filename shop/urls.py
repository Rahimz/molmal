from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


app_name = 'shop'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('prices/', views.price_view, name='price_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('', cache_page(60 * 15)(views.home), name='home'),
]
