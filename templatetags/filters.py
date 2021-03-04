from django import template

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


# @register.inclusion_tag('tdcp/field_render.html')
# def render(field):
#     return {'field': field}