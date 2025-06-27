from django import template

from gearcore.wishlist.models import WishlistItem

register = template.Library()

@register.simple_tag(takes_context=True)
def user_wishlist_ids(context):
    user = context.get('request').user
    product_ids = set(
        WishlistItem.objects.filter(wishlist__user=user)
        .values_list('product_id', flat=True)
    )
    return product_ids

