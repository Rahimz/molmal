from django.db import models
from django.conf import settings
import datetime
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    # In order to keep your code generic, use the get_user_model()
    # method to retrieve the user model and the AUTH_USER_MODEL setting
    # to refer to it when defining a model's relations to the user model,
    # instead of referring to the auth user model directly.
    GENDER_CHOICES = (('male', 'Male'),
                      ('female', 'Female'),
                      ('others', 'Others'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    gender = models.CharField(verbose_name='Gender',
                              max_length=50,
                              default='others',
                              choices=GENDER_CHOICES,)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                      on_delete=models.CASCADE,
                      related_name='address')
    fav_address = models.BooleanField(default=False)
    first_name = models.CharField(_('first name'),
                                  max_length=50, blank=True, null=True)
    last_name = models.CharField(_('last name'),
                                 max_length=50)
    phone = models.CharField(_('Phone'),max_length=12)
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)

    def __str__(self):
        return self.address[:30]
