from django.urls import path
from . import views


app_name = 'pages'

urlpatterns = [
    path('<slug:slug>/', views.PageView, name='page_view'),
]
