import json

from django.http import JsonResponse
from allauth.core.internal.httpkit import redirect
from django.template.loader import render_to_string

from gearcore.carts.models import Cart
from gearcore.carts import utils
from gearcore.goods.models import Products


def cart_add(request):
    data = json.loads(request.body)

    slug = data.get('slug', None)

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

    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if carts.exists():
            cart = carts.first()
            if not cart:
                raise ValueError('немає такого кошика')
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

    user_carts = utils.get_user_carts(request)

    carts_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': user_carts}, request=request)

    return JsonResponse(
        {
            'status': 200,
            'debug_message': "успішно додано до кошику",
            'html': carts_items_html,
        }
    )


def cart_change(request):
    data = json.loads(request.body)

    action = data.get('action', None)
    id_cart = data.get('id_cart', None)

    if not data or not action or not id_cart:
        return JsonResponse(
            {
                'status': 404,
                'debug_message': 'не отримано даних для зміни кількості',
                'html': None,
            }
        )

    cart = Cart.objects.get(id=id_cart)

    if not cart:
        return JsonResponse(
            {
                'status': 404,
                'debug_message': 'не вдалося отримати потрібний кошик',
                'html': None,
            }
        )

    if action == 'increment':
        cart.quantity += 1
        cart.save()
    elif action == 'decrement':
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    else:
        return JsonResponse(
            {
                'status': 404,
                'debug_message': 'не зрозуміла дія над кошиком',
                'html': None,
            }
        )

    user_carts = utils.get_user_carts(request)

    carts_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': user_carts}, request=request)

    return JsonResponse(
        {
            'status': 200,
            'debug_message': "успішно оновлено кількість",
            'html': carts_items_html,
        }
    )


def cart_remove(request):
    data = json.loads(request.body)
    id_cart = data.get('id_cart', None)
    cart = Cart.objects.get(id=id_cart)
    cart.delete()

    user_carts = utils.get_user_carts(request)

    carts_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': user_carts}, request=request)

    return JsonResponse(
        {
            'status': 200,
            'debug_message': "успішно видалено кошик",
            'html': carts_items_html,
        }
    )
