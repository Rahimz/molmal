from django import template
from pages.models import Page


register = template.Library()

@register.inclusion_tag('shop/pages/footer_pages.html')
def footer_pages():
    footer_pages = Page.objects.all().filter(active=True)
    return {'footer_pages': footer_pages}
