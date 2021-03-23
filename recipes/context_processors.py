from django.shortcuts import get_object_or_404

from recipes.models import Recipe


def tags_for_paginator_link(request):
    request_args = request.GET.getlist('tags')
    output = ''
    if request_args:
        for arg in request_args:
            output = f'{output}&tags={arg}'
    return {
        'tags_for_paginator_link': output
    }


def recipe_ingredients(request):
    recipe_id = request.resolver_match.kwargs.get('pk')
    if recipe_id:
        recipe = get_object_or_404(
            Recipe.objects.prefetch_related('ingredients'),
            id=recipe_id
        )
        recipe_ingrs = recipe.ingredients.all()
        recipe_amounts = recipe.amounts.all()
        current_ingrs = []
        for idx, ingr in enumerate(recipe_ingrs, 1):
            amount = recipe_amounts.get(ingredient=ingr.id)
            current_ingrs.append((idx, ingr, amount.value))
        return {'recipe_ingredients': current_ingrs}
    return {'recipe_ingredients': None}


# @register.inclusion_tag('recipes/aux/render_filter.html')
# def render_filter(items):
#     data = []
#     for item in items:
#         name = item.data['value'].value
#         obj = Tag.objects.get(name=name)
#         item.data['attrs']['class'] = (
#             f'tags__checkbox tags__checkbox_style_{obj.color}'
#         )
#         data.append((item, obj))
#     return {'items': data}
