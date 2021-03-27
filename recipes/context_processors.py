from recipes.models import Tag


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


def all_tags(request):
    return {
        'all_tags': Tag.objects.all().order_by('id')
    }
