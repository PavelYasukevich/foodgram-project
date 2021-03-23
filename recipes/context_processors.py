from recipes.models import Tag


def shop_list_size(request):
    if request.user.is_authenticated:
        count = request.user.purchases.all().count()
    else:
        count = 0
    return {
        'shop_list_size': count
    }


def request_args(request):
    return {
        'request_args': request.GET.getlist('tags')
    }



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
