from django.contrib import admin
from .models import DeliveryContainer

@admin.register(DeliveryContainer)
class DeliveryContainerAdmin(admin.ModelAdmin):
    list_display = ['fa_date', 'fa_time', 'order_in_container', 'start', 'end']
    list_filter = ['fa_date', 'fa_time']
