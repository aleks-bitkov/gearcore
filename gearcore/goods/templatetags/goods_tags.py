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


# Альтернативный вариант с defaultdict (более компактно):
# def categories_compact():
#     raw_categories = CategoryBrand.objects.all()
#     categories_dict = defaultdict(list)
#
#     for model in raw_categories:
#         categories_dict[model.category].append(model.brand)
#
#     return dict(categories_dict)
