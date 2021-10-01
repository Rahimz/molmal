from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns =[
    path('<int:pk>/', views.delivery_selection, name="delivery_selection")
]
