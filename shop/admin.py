from django.contrib import admin
from .models import Category, Product, Slider, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'stock']
    list_filter = ['available', ]
    list_editable = ['price', 'available', 'stock', 'slug']
    prepopulated_fields = {'slug': ('name',), 'image_alt': ('name',)}
    ordering = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'product', 'active')
    list_filter = ('active', 'user', 'product' )
    search_fields = ('product', 'user', 'name')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    # list_editable = ['title', 'active']
    list_filter = ['title', 'active']


# use memcache admin index site
admin.site.index_template = 'memcache_status/admin_index.html'
