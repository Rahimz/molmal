from django.contrib import admin
from .models import Category, Product, Slider

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'temp_product','stock']
    list_filter = ['available', ]
    list_editable = ['price', 'available', 'temp_product', 'stock', 'slug']
    prepopulated_fields = {'slug': ('name',), 'image_alt': ('name',)}
    ordering = ['name']

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    # list_editable = ['title', 'active']
    list_filter = ['title', 'active']


# use memcache admin index site
admin.site.index_template = 'memcache_status/admin_index.html'
