from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from django.conf import settings
from . import views


app_name = 'shop'

# THe if statement is for disableing cache in local env
if settings.DEBUG:
    urlpatterns = [
        path('products/', views.product_list, name='product_list'),
        path('prices/', views.price_view, name='price_list'),
        path('search/', views.product_search, name='product_search'),
        path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
        # TODO:: Farsi slug does not work
        # re_path(r'(?P<category_slug>\w+)$', views.product_list, name='product_list_by_category'),
        path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
        path('', views.home, name='home'),
    ]
else:
    urlpatterns = [
        path('products/', cache_page(60 * 10)(views.product_list), name='product_list'),
        path('prices/', views.price_view, name='price_list'),
        path('search/', views.product_search, name='product_search'),
        path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
        path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
        path('', cache_page(60 * 10)(views.home), name='home'),
    ]
