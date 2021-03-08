from django import template

from recipes.models import Tag

register = template.Library()

# @register.filter
# def get_fields(obj):
#     return [
#         (field.verbose_name, field.value_to_string(obj))
#         for field in obj._meta.fields
#         if field.name not in ('id', 'vendor', 'cb_type')
#     ]

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


# @register.filter
# def addstyle(field, css):
#     return field.as_widget(attrs={"style": css})


# @register.filter
# def label_with_tooltip(value, txt):
#     return value.label_tag(attrs={'data-tooltip': txt})


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
