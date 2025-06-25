from django.utils.http import urlencode

from django import template

from gearcore.goods.models import Motorcycle

register = template.Library()


@register.simple_tag()
def categories_tag():
    motorcycles = Motorcycle.objects.select_related('category', 'brand').all()

    categories_dict = {}

    for moto in motorcycles:
        category = moto.category
        brand = moto.brand

        if category not in categories_dict:
            categories_dict[category] = set()
        categories_dict[category].add(brand)

    for category in categories_dict:
        categories_dict[category] = list(categories_dict[category])

    return categories_dict

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context.get('request').GET.dict()
    query.update(kwargs)
    return urlencode(query)


# Альтернативный вариант с defaultdict (более компактно):
# def categories_compact():
#     raw_categories = CategoryBrand.objects.all()
#     categories_dict = defaultdict(list)
#
#     for model in raw_categories:
#         categories_dict[model.category].append(model.brand)
#
#     return dict(categories_dict)
