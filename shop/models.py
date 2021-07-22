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
    MEASURES =(('gram', 'گرم'),
               ('kilogram', 'کیلوگرم'),
               ('litre', 'لیتر'),)

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,)
    name = models.CharField(max_length=1000, db_index=True)
    slug = models.SlugField(max_length=1000, db_index=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/images/',
                              blank=True)
    image_alt = models.CharField(max_length=300,
                                 blank=True,
                                 null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField(default=0)
    weight = models.FloatField(default=0,
                                 null=True, blank=True)
    weight_measure = models.CharField(max_length=50,
                                      choices=MEASURES,
                                      null=True, blank=True)
    available = models.BooleanField(default=True)
    # For Temporary home page
    temp_product = models.BooleanField(default=False,
                                       null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
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
