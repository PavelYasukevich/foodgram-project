from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Tag

from . import services


def selected_filters(request):
    request_args = request.GET.getlist('tags')
    return {
        'selected_filters': request_args
    }


def tags_for_paginator_link(request):
    request_args = request.GET.getlist('tags')
    output = ''
    if request_args:
        for arg in request_args:
            output = f'{output}&tags={arg}'
    return {
        'tags_for_paginator_link': output
    }


def recipe_ingredients(request):
    url = request.resolver_match.url_name
    if url == 'new_recipe':
        valid_ingrs, _ = services._check_form_ingrs(request.POST)
        return {'recipe_ingredients': valid_ingrs}

    recipe_id = request.resolver_match.kwargs.get('pk')
    if recipe_id:
        recipe = get_object_or_404(
            Recipe.objects.prefetch_related('ingredients'),
            id=recipe_id
        )
        recipe_ingrs = recipe.ingredients.all()
        recipe_amounts = recipe.amounts.all()
        current_ingrs = []
        for idx, ingr in enumerate(recipe_ingrs, 1):
            amount = recipe_amounts.get(ingredient=ingr.id)
            current_ingrs.append((idx, ingr, amount.value))
        return {'recipe_ingredients': current_ingrs}

    return {'recipe_ingredients': None}


def all_tags(request):
    return {
        'all_tags': Tag.objects.all().order_by('id')
    }
