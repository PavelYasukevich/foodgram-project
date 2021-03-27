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
    """Вернуть отфильтрованный по тегам queryset."""
    queryset = Recipe.objects.annotated(user=request.user)
    tags = request.GET.getlist('tags')
    if tags:
        for tag in tags:
            if tag in (Tag.BREAKFAST, Tag.LUNCH, Tag.DINNER):
                queryset = queryset.filter(tags__name__contains=tag)
    return queryset
