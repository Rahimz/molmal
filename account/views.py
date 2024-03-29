from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm,  ProfileEditForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Address
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

    addresses = Address.objects.filter(user=user)
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
                 'orders': orders,
                 'addresses': addresses})



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

@login_required
def address_detail(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        address_form = AddressForm(instance=address,
                                data=request.POST)

        if address_form.is_valid():

            cd = address_form.cleaned_data['address']

            if address.fav_address:
                addresses = Address.objects.filter(user=request.user).exclude(pk=address.pk)
                for addry in addresses:
                    addry.fav_address = False
                    addry.save()
            address_form.save()
            # https://docs.djangoproject.com/en/2.0/ref/contrib/messages/
            messages.success(request,
                            'Address updated successfully')
        else:
            messages.error(request, 'Error updating your address')
    else:
        address_form = AddressForm(instance=address)

    return render(request,
                  'account/address_detail.html',
                  {'address': address,
                  'address_form': address_form})

@login_required
def add_address(request):

    if request.method == 'POST':
        address_form = AddressForm(data=request.POST)

        if address_form.is_valid():
            print('hi')
            new_address = address_form.save(commit=False)

            new_address.user = request.user

            if new_address.fav_address:
                print('hi')
                addresses = Address.objects.filter(user=request.user).exclude(pk=new_address.pk)
                for addry in addresses:
                    addry.fav_address = False
                    addry.save()

            new_address.save()

            messages.success(request,
                            'Address added successfully')
            return redirect('/account/dashboard/#address-section')
        else:
            messages.error(request,
                            'Address is not added')
    else:
        address_form = AddressForm()
    return render(request,
                  'account/add_address.html',
                  {'address_form': address_form})


# @login_required
# def address_delete(request, pk) :
#     address_to_delete = get_object_or_404(Address, pk=pk) #.delete()
#     return reverse('/dashboard')
