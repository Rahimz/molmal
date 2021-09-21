from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # include all url we need for registration
    path('', include('django.contrib.auth.urls')),
    # user registration url
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('add-profile/', views.create, name='add'),

]
