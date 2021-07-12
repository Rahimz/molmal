from django.db import models
from django.urls import reverse


class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique=True,
                            allow_unicode=True)
    text = models.TextField()
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('pages:page_view',
                        args=[self.slug])
