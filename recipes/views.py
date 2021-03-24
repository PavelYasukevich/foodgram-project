from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_pdfkit import PDFView

from . import services
from .context_processors import tags_for_paginator_link
from .forms import RecipeForm
from .models import Favorite, Purchase, Recipe

User = get_user_model()


class RecipePostMixin:
    """Содержит общую логику обработки создания и редактирования рецепта."""

    def get_form_kwargs(self):
        result = super().get_form_kwargs()
        result['request'] = self.request
        return result

    def post(self, request, *args, **kwargs):
        ingrs, form = services.get_ingr_list_from_request_data(
            data=self.request.POST,
            form=self.get_form(),
        )
        if form.is_valid():
            return self.form_valid(form, ingrs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, ingrs):
        self.object = form.save()
        services.create_amount_objects_and_add_ingrs_to_recipe(
            recipe=self.object,
            ingrs=ingrs,
        )
        return redirect(self.get_success_url())


class PaginatorRedirectMixin:
    """
    Редирект на последнюю существущую страницу.

    Возвращает последнюю страницу, если номер запрошенной страницы
    превышает общее количество страниц пагинатора, или введены некорректные
    данные в гет-параметр вручную.
    """

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            queryset = self.get_queryset()
            paginator = self.get_paginator(
                queryset,
                self.get_paginate_by(queryset),
                orphans=self.get_paginate_orphans(),
                allow_empty_first_page=self.get_allow_empty()
            )
            tags = tags_for_paginator_link(request)['tags_for_paginator_link']
            url = reverse('index')
            return redirect(f'{url}?page={paginator.num_pages}{tags}')


class IndexView(PaginatorRedirectMixin, ListView):
    """Главная страница со списком всех рецептов сайта."""

    context_object_name = 'recipes'
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/index.html'

    def get_queryset(self):
        return services.get_filtered_queryset(self.request)


class RecipeDetailView(DetailView):
    """Страница отдельного рецепта."""

    context_object_name = 'recipe'
    template_name = 'recipes/singlePage.html'

    def get_queryset(self):
        return services.get_filtered_queryset(self.request)


class ProfileView(PaginatorRedirectMixin, ListView):
    """Страница рецептов отдельного автора."""

    context_object_name = 'author_recipes'
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/authorRecipe.html'

    def get_queryset(self):
        queryset = services.get_filtered_queryset(self.request).filter(
            author__id=self.kwargs.get('id')
        )
        return queryset


class SubscriptionsView(LoginRequiredMixin, PaginatorRedirectMixin, ListView):
    """Список авторов, на которых подписан пользователь."""

    context_object_name = 'subscriptions'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/myFollow.html'

    def get_queryset(self):
        return self.request.user.subscriptions.select_related('author')


class CreateRecipeView(LoginRequiredMixin, RecipePostMixin, CreateView):
    """Страница создания нового рецепта."""

    context_object_name = 'recipe'
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class UpdateRecipeView(LoginRequiredMixin, RecipePostMixin, UpdateView):
    """Страница редактирования рецепта автором."""

    context_object_name = 'recipe'
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'
    queryset = Recipe.objects.all()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class FavoritesView(LoginRequiredMixin, PaginatorRedirectMixin, ListView):
    """Список избранных рецептов пользователя."""

    context_object_name = 'favorites'
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/favorite.html'

    def get_queryset(self):
        return services.get_filtered_queryset(
            self.request).filter(in_favored=True)


class PurchasesView(LoginRequiredMixin, ListView):
    """Список покупок пользователя."""

    context_object_name = 'purchases'
    ordering = '-pub_date'
    template_name = 'recipes/purchaseList.html'

    def get_queryset(self):
        return services.get_filtered_queryset(
            self.request).filter(in_purchased=True)


class DownloadShoppingList(LoginRequiredMixin, PDFView):
    """Загрузка сформированного файла со списком покупок пользователя."""

    template_name = 'recipes/aux/shopping_list.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        purchase_list = services.make_purchase_list_for_download(
            user=self.request.user
        )
        kwargs.update({'purchase_list': purchase_list})
        return kwargs


class DeleteRecipeView(LoginRequiredMixin, DeleteView):
    """Страница подтверждения удаления рецепта автором."""

    model = Recipe
    template_name = 'recipes/deleteRecipe.html'
    success_url = reverse_lazy('index')


def page_not_found(request, exception):
    """Вернуть страницу ошибки 404."""
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    """Вернуть страницу ошибки 500."""
    return render(request, 'misc/500.html', status=500)
