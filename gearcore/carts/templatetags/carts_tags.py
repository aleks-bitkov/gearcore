from django import template

from gearcore.carts import utils

register = template.Library()

@register.simple_tag
def user_carts(request):
    return utils.get_user_carts(request)

