from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm,  ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from orders.models import Order, OrderItem
import datetime


@login_required
def dashboard(request):
    user = request.user

    # we grab all orders when each user request dashboard
    # then we updated all unpaid order and make them inactive
    # orders = Order.objects.filter(active=True)
    orders = Order.objects.filter(user=request.user, active=True)

    # This function clean every order that
    # does not pay after 24 hours.
    # It dose not work in cron job and move to here
    for order in orders:
        if datetime.datetime.now().date().day - order.created.day > 1 and order.paid == False:
            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                product = order_item.product
                product.stock += order_item.quantity
                product.save()
            order.active = False
            order.save()


    return render(request,
                'account/dashboard.html',
                {'profile': user.profile,
                 'orders': orders})



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                         'account/register_done.html',
                         {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # https://docs.djangoproject.com/en/2.0/ref/contrib/messages/
            messages.success(request,
                            'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                'account/edit.html',
                {'user_form': user_form,
                'profile_form': profile_form})


@login_required
def create(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request,
                            'Profile added successfully')
            return render(request,
                          'account/dashboard.html',
                          {'profile': new_profile,}
                          )
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm()

    return render(request,
                'account/create_profile.html',
                {'user_form': user_form,
                 'profile_form': profile_form})
