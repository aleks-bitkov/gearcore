from django.utils.http import urlencode

from django import template

from gearcore.goods.models import CategoryBrand

register = template.Library()


@register.simple_tag()
def categories_tag():
    raw_categories = CategoryBrand.objects.all()
    categories_dict = {}

    for model in raw_categories:
        if model.category in categories_dict:
            categories_dict[model.category].append(model.brand)
        else:
            categories_dict[model.category] = [model.brand]

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
