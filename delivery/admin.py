from django.contrib import admin
from .models import DeliveryContainer

@admin.register(DeliveryContainer)
class DeliveryContainerAdmin(admin.ModelAdmin):
    list_display = ['start', 'end']
    
