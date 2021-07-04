from django.contrib import admin
from .models import Category, Product, Slider

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated', 'temp_product']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'temp_product']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    # list_editable = ['title', 'active']
    list_filter = ['title', 'active']
