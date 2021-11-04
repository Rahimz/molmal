from django.contrib import admin
from .models import Profile, Address


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'fav_address', 'address']
