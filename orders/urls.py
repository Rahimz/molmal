from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('my-orders/<int:order_id>/', views.user_order_detail, name='user_order_detail'),
    path('my-orders/repay/<int:order_id>/', views.order_repay, name='order_repay'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]
