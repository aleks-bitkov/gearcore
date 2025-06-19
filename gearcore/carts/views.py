from allauth.core.internal.httpkit import redirect
from django.shortcuts import render

from gearcore.carts.models import Cart
from gearcore.goods.models import Products


def cart_add(request, slug):
    product = Products.objects.get(slug=slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if not cart:
                raise ValueError('немає кошика')
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    return redirect(request.META.get('HTTP_REFERER'))

def cart_change(request):
    ...

def cart_remove(request):
    ...
