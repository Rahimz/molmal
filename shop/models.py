from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=500,
                            db_index=True,)
    slug = models.SlugField(max_length=500,
                            unique=True,
                            allow_unicode=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,)
    name = models.CharField(max_length=1000, db_index=True)
    slug = models.SlugField(max_length=1000, db_index=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/images/',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    available = models.BooleanField(default=True)
    # For Temporary home page
    temp_product = models.BooleanField(default=False,
                                       null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    def __str__(self):
        return self.name


class Slider(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500,
                                   null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='sliders/')
    active = models.BooleanField(default=True)
