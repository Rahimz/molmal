from django.shortcuts import reverse
from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _
# https://github.com/slashmili/django-jalali
from django_jalali.db import models as jmodels
from django.conf import settings
from cart.cart import Cart


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             blank=True, null=True)
    first_name = models.CharField(_('first name'),
                                  max_length=50, blank=True, null=True)
    last_name = models.CharField(_('last name'),
                                 max_length=50)
    phone = models.CharField(max_length=12, blank=True, null=True)
    fa_date = jmodels.jDateField(null=True, blank=True)
    email = models.EmailField(_('e-mail'), blank=True, null=True)
    address = models.CharField(
        _('address'), max_length=250, blank=True, null=True)
    postal_code = models.CharField(
        _('postal code'), max_length=20, blank=True, null=True)
    city = models.CharField(_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    # if the coupon gets deleted,
    # the coupon field is set to Null,
    # but the discount is preserved
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))

    def get_absolute_url(self):
        return reverse('orders:user_order_detail',
                       args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class OrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='orderhistory')
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return order.last_name
