from recipes.models import Tag


def tags_for_paginator_link(request):
    request_args = request.GET.getlist('tags')
    output = ''
    if request_args:
        for arg in request_args:
            output = f'{output}&tags={arg}'
    return {
        'tags_for_paginator_link': output
    }



# @register.simple_tag
# def add_filter(request_args):
#     output = ''
#     if request_args:
#         for arg in request_args:
#             output = f'{output}&tags={arg}'
#     return output


# @register.inclusion_tag(
#     'recipes/aux/render_edit_recipe_ingrs.html',
#     name='edit_recipe_ingrs'
# )
# @register.inclusion_tag(
#     'recipes/aux/render_single_recipe_ingrs.html',
#     name='single_recipe_ingrs'
# )
# def render_recipe_edit_ingrs(recipe):
#     current_ingrs = []
#     recipe_ingrs = recipe.ingredients.all()
#     recipe_amounts = recipe.amounts.all()
#     for idx, ingr in enumerate(recipe_ingrs, 1):
#         amount = recipe_amounts.get(ingredient=ingr.id)
#         current_ingrs.append((idx, ingr, amount.value))
#     return {'current_ingrs': current_ingrs}


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
