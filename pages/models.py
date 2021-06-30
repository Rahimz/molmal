from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique=True,
                            allow_unicode=True)
    text = models.TextField()
