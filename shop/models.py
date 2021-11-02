from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=500,
                            db_index=True,)
    slug = models.SlugField(max_length=500,
                            unique=True,
                            allow_unicode=True)
    image = models.ImageField(upload_to='categories/images',
                              null=True,
                              blank=True)

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
    short_description = models.CharField(max_length=250,
                                         default='',
                                         blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField(default=0)
    weight = models.FloatField(default=0,
                                 null=True, blank=True)
    weight_measure = models.CharField(max_length=50,
                                      choices=MEASURES,
                                      null=True, blank=True)
    available = models.BooleanField(default=True)

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


class Comment(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             blank=True, null=True)
    name = models.CharField(_('Name'),max_length=80)
    email = models.EmailField(_('Email'),)
    body = models.TextField(_('Comment'),)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default= False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.product)
