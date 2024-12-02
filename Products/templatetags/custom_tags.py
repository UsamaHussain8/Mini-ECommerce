from django import template

register = template.Library()

@register.filter
def product_image_url(image_url):
    return f"/products{image_url}"
