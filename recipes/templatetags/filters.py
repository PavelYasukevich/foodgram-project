from django import template
from django.contrib.auth import get_user_model

from recipes.models import Favorite, Purchase, Subscription, Tag

User = get_user_model()
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


TENSES = {
    1: '',
    2: 'а',
    3: 'а',
    4: 'а',
}


@register.filter
def tense(text, count):
    end = int(count) % 100
    end = end if end in (11, 12, 13, 14) else end % 10
    end = TENSES.get(end, "ов")
    return f'{text}{end}'


@register.filter
def in_subscriptions(author, user):
    return Subscription.objects.filter(author=author, user=user).exists()
#   return user in author.subscribers


@register.filter
def in_favorites(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user).exists()
#   return user.id in recipe.favored_by


@register.filter
def in_purchases(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()
#   return user.id in recipe.purchased_by


@register.simple_tag
def add_filter(request_args):
    output = ''
    if request_args:
        for arg in request_args:
            output = f'{output}&tags={arg}'
    return output


@register.inclusion_tag(
    'recipes/aux/render_edit_recipe_ingrs.html',
    name='edit_recipe_ingrs'
)
@register.inclusion_tag(
    'recipes/aux/render_single_recipe_ingrs.html',
    name='single_recipe_ingrs'
)
def render_recipe_edit_ingrs(recipe):
    current_ingrs = []
    recipe_ingrs = recipe.ingredients.all()
    recipe_amounts = recipe.amounts.all()
    for idx, ingr in enumerate(recipe_ingrs, 1):
        amount = recipe_amounts.get(ingredient=ingr.id)
        current_ingrs.append((idx, ingr, amount.value))
    return {'current_ingrs': current_ingrs}


@register.inclusion_tag('recipes/aux/render_filter.html')
def render_filter(items):
    data = []
    for item in items:
        name = item.data['value'].value
        obj = Tag.objects.get(name=name)
        item.data['attrs']['class'] = (
            f'tags__checkbox tags__checkbox_style_{obj.color}'
        )
        data.append((item, obj))
    return {'items': data}
