from django import template

from recipes.models import Tag, Recipe


register = template.Library()

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.inclusion_tag('recipes/aux/render_tags.html')
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


@register.inclusion_tag('recipes/aux/render_tags.html')
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


@register.inclusion_tag('recipes/aux/render_edit_recipe_ingrs.html', name='edit_recipe_ingrs')
@register.inclusion_tag('recipes/aux/render_single_recipe_ingrs.html', name='single_recipe_ingrs')
def render_recipe_edit_ingrs(recipe):
    current_ingrs = []
    recipe_ingrs = recipe.ingredients.all()
    recipe_amounts = recipe.amounts.all()
    for idx, ingr in enumerate(recipe_ingrs, 1):
        amount = recipe_amounts.get(ingredient=ingr.id)
        current_ingrs.append((idx, ingr, amount.value))
    return {'current_ingrs': current_ingrs}
