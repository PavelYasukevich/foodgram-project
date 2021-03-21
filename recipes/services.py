from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Amount, Ingredient, Recipe

User = get_user_model()


def make_purchase_list_for_download(user) -> dict:
    """
    Сформировать словарь вида {'ингредиент': 'количество'} для передачи
    в шаблон для скачивания.
    """
    purchases = user.purchases.select_related('recipe').all()
    purchase_list = {}
    for purchase in purchases:
        ingredients = purchase.recipe.ingredients.all()
        for ingr in ingredients:
            amount = Amount.objects.get(
                recipe=purchase.recipe, ingredient=ingr
            ).value
            purchase_list[ingr] = purchase_list.get(ingr, 0) + amount
        return purchase_list


def get_recipes_queryset_filtered_by_tags(user_id=None, model=None, tags=None):
    """Вернуть список рецептов отфильтрованный по тегам запроса."""
    if user_id is not None:
        queryset = _get_user_related_recipes(user_id, model)
    else:
        queryset = Recipe.objects.all()
    queryset = _filter_queryset_by_tags(queryset, tags)
    return queryset


def _get_user_related_recipes(user_id, model=None):
    """
    Вернуть список рецептов, относящихся к пользователю через переданную
    модель, или рецепты его авторства, если модель не передана.
    """
    user = get_object_or_404(User, id=user_id)
    if model is not None:
        user_related_objects = model.objects.filter(
            user=user).values_list('recipe__id', flat=True)
        queryset = Recipe.objects.filter(id__in=user_related_objects)
    else:
        queryset = Recipe.objects.filter(author=user)
    return queryset


def _filter_queryset_by_tags(queryset, tags):
    """Отфильтровать queryset по тегам."""
    if tags is not None:
        for tag in tags:
            queryset = queryset.filter(tags__name__contains=tag)
    return queryset


def get_ingr_list_from_request_data(data: dict, form):
    '''
    Вернуть список ингредиентов создаваемого рецепта, добавляет в форму
    ошибки, если указанных ингредиентов нет в существующем перечне на сайте.
    '''
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
    Добавить non_field ошибку в форму.Используется для валидации
    поля с ингредиентам, т.к оно не входит в поля формы рецепта.
    '''
    form.add_error(None, error_msg)


def create_amount_objects_and_add_ingrs_to_recipe(recipe, ingrs):
    '''
    Создать объекты Amount в базе и добавить ингредиенты из списка в рецепт.
    '''
    Amount.objects.filter(recipe=recipe).delete()
    for ingr, amount_value in ingrs:
        Amount.objects.create(
            value=amount_value, recipe=recipe, ingredient=ingr
        )
        recipe.ingredients.add(ingr)


def get_user_subscriptions_list(user_id):
    '''Вернуть список авторов, на которых подписан пользователь.'''
    user = get_object_or_404(User, id=user_id)
    queryset = User.objects.filter(subscribers__user__id=user.id)
    return queryset
