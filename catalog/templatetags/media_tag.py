import os.path

from django import template

from config.settings import BASE_DIR

register = template.Library()


@register.filter()
def media_tag(path):
    if path:
        return f"media/{path}"
    return f'media/image_not_found.jpg'

