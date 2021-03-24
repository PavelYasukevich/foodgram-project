from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .models import Amount, Ingredient, Recipe

User = get_user_model()


def make_purchase_list_for_download(user):
    """Сформировать ингредиенты для скачивания."""
    ingredients = user.purchases.select_related('recipe').prefetch_related(
        'recipe__ingredients').order_by(
        'recipe__ingredients__name').values_list(
        'recipe__ingredients__name',
        'recipe__ingredients__measurement_unit').annotate(
        amount=Sum('recipe__amounts__value'))
    return ingredients


def get_filtered_queryset(request):
    queryset = Recipe.objects.annotated(user=request.user)
    tags=request.GET.getlist('tags')
    if tags:
        queryset = _filter_queryset_by_tags(
            queryset=queryset,
            tags=tags
        )
    return queryset


def _filter_queryset_by_tags(queryset, tags):
    """Отфильтровать queryset по тегам."""
    if tags is not None:
        for tag in tags:
            queryset = queryset.filter(tags__name__contains=tag)
    return queryset


def get_ingr_list_from_request_data(data, form):
    '''Вернуть список ингредиентов создаваемого рецепта.'''
    ingrs = list()
    for html_name, ingredient_name in data.items():
        if html_name.startswith('nameIngredient_'):
            ingr_to_add = Ingredient.objects.filter(name=ingredient_name)
            if ingr_to_add.exists():
                number_at_the_end = int(html_name.split('_')[1])
                amount_value = int(
                    data.get(f'valueIngredient_{number_at_the_end}')
                )
                ingrs.append((ingr_to_add.first(), amount_value))
            else:
                _add_non_field_error_to_form(
                    form=form,
                    error_msg=f'''Ингредиент {ingredient_name} не найден.
                        Пожалуйста, выберите из списка существующих
                        ингредиентов.''',
                )
    if not ingrs:
        _add_non_field_error_to_form(
            form=form,
            error_msg='Не указано ни одного ингредиента \
                        из существующего перечня',
        )
    return ingrs, form


def _add_non_field_error_to_form(form, error_msg):
    '''
    Добавить non_field ошибку в форму.

    Используется для валидации поля с ингредиентам, т.к оно не входит
    в поля формы рецепта.
    '''
    form.add_error(None, error_msg)
