from django.contrib.auth import get_user_model
from django.db.models import Sum

from .models import Ingredient, Recipe, Tag

User = get_user_model()


def make_purchase_list_for_download(user):
    """Сформировать ингредиенты для скачивания."""
    ingredients = (
        user.purchases.select_related("recipe")
        .prefetch_related("recipe__ingredients")
        .order_by("recipe__ingredients__name")
        .values_list(
            "recipe__ingredients__name",
            "recipe__ingredients__measurement_unit",
        )
        .annotate(amount=Sum("recipe__amounts__value"))
    )
    return ingredients


def get_filtered_queryset(request):
    """
    Вернуть отфильтрованный по тегам queryset.

    Аннотирует рецепты признаками наличия в избранном и покупках, если
    пользователь авторизован, фильтрует по тегам запроса, при их наличии.
    """
    queryset = Recipe.objects.annotated(user=request.user)
    tags = request.GET.getlist('tags')
    if tags:
        queryset = _filter_queryset_by_tags(queryset=queryset, tags=tags)
    return queryset


def _filter_queryset_by_tags(queryset, tags):
    """Отфильтровать queryset по тегам."""
    for tag in tags:
        if tag in Tag.CHOICES:
            queryset = queryset.filter(tags__name__contains=tag)
    return queryset


def handle_form_ingredients(data, form):
    """
    Обработка ингредиентов из формы.

    Вернуть список валидных ингредиентов (присутствующих в существующем
    перечне) и при наличии ошибок - добавить их в форму.
    """
    valid_ingrs, errors = _check_form_ingrs(data)
    _add_non_field_error_to_form(form, errors)
    return valid_ingrs


def _check_form_ingrs(data):
    """Получить валидный список ингредиентов и ошибки формы."""
    form_ingrs = _get_ingr_list_from_request_data(data)
    ingrs_to_add = Ingredient.objects.filter(name__in=form_ingrs)
    has_wrong_ingrs = ingrs_to_add.count() != len(form_ingrs)
    errors = []

    if has_wrong_ingrs:
        errors.append('Пожалуйста, выбирайте только из списка \
            существующих ингредиентов.')

    if not form_ingrs:
        errors.append('Не указано ни одного ингредиента \
            из существующего перечня')

    valid_ingrs = [
        (idx, ingr, form_ingrs[ingr.name])
        for idx, ingr
        in enumerate(ingrs_to_add)
    ]
    return valid_ingrs, errors


def _get_ingr_list_from_request_data(data):
    """Вернуть словарь ингредиентов создаваемого рецепта."""
    form_ingrs = dict()
    for html_name, ingredient_name in data.items():
        if html_name.startswith('nameIngredient_'):
            number_at_the_end = int(html_name.split('_')[1])
            form_ingrs[ingredient_name] = form_ingrs.get(
                ingredient_name, 0) + int(
                data.get(f'valueIngredient_{number_at_the_end}')
            )
    return form_ingrs


def _add_non_field_error_to_form(form, errors):
    """
    Добавить non_field ошибку в форму.

    Используется для валидации поля с ингредиентам, т.к оно не входит
    в поля формы рецепта.
    """
    for error in errors:
        form.add_error(None, error)
