from django import template

from recipes.models import Tag, Recipe


register = template.Library()

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.inclusion_tag('recipes/render_tags.html')
def render_recipe_form_tags(items):
    for item in items:
        _id = item.data['value'].value
        if _id == 1:
            item.data['attrs']['class'] = 'tags__checkbox tags__checkbox_style_orange'
        if _id == 2:
            item.data['attrs']['class'] = 'tags__checkbox tags__checkbox_style_green'
        if _id == 3:
            item.data['attrs']['class'] = 'tags__checkbox tags__checkbox_style_purple'
    return {'items': items}


@register.inclusion_tag('recipes/render_tags.html')
def render_recipe_edit_tags(items, recipe):
    recipe_tags = list(recipe.tags.values_list('id', flat=True))
    for item in items:
        _id = item.data['value'].value
        if _id in recipe_tags:
            item.data['attrs']['checked'] = True
        if _id == 1:
            item.data['attrs']['class'] = 'tags__checkbox tags__checkbox_style_orange'
        if _id == 2:
            item.data['attrs']['class'] = 'tags__checkbox tags__checkbox_style_green'
        if _id == 3:
            item.data['attrs']['class'] = 'tags__checkbox tags__checkbox_style_purple'
    return {'items': items}


@register.inclusion_tag('recipes/render_edit_recipe_ingrs.html')
def render_recipe_edit_ingrs(recipe):
    current_ingrs = []
    recipe_ingrs = recipe.ingredients.all()
    recipe_amounts = recipe.amounts.all()
    print(recipe)
    print(recipe_ingrs)
    print(recipe_amounts)
    for idx, ingr in enumerate(recipe_ingrs, 1):
        amount = recipe_amounts.get(ingredient=ingr.id)
        current_ingrs.append((idx, ingr, amount.value))
    print(current_ingrs)
    return {'current_ingrs': current_ingrs}

