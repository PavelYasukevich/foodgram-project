from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import InvalidPage
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_pdfkit import PDFView
from pytils.translit import slugify

from . import services
from .forms import FilterForm, RecipeForm
from .models import Favorite, Purchase, Recipe

User = get_user_model()


class RecipePostMixin:
    """Содержит общую логику обработки создания и редактирования рецепта."""

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
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.slug = slugify(self.object.name)
        self.object.save()
        services.create_amount_objects_and_add_ingrs_to_recipe(
            recipe=self.object,
            ingrs=ingrs,
        )
        form.save_m2m()
        return redirect(self.get_success_url())


class PaginatorRedirectMixin:
    """
    Редирект на последнюю существущую страницу.

    Возвращает последнюю страницу, если номер запрошенной страницы
    превышает общее количество страниц пагинатора, или введены некорректные
    данные в гет-параметр вручную.
    """

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_kwarg = self.page_kwarg
        page = (
            self.kwargs.get(page_kwarg)
            or self.request.GET.get(page_kwarg)
            or 1
        )
        try:
            page_number = int(page)
            page = paginator.page(page_number)
        except (ValueError, InvalidPage):
            page_number = paginator.num_pages
            page = paginator.page(page_number)
        return (paginator, page, page.object_list, page.has_other_pages())


class IndexView(PaginatorRedirectMixin, ListView):
    """Главная страница со списком всех рецептов сайта."""

    context_object_name = 'recipes'
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterform'] = FilterForm(self.request.GET)
        context['req_args'] = self.request.GET.getlist('tags')
        return context

    def get_queryset(self):
        queryset = services.get_recipes_queryset_filtered_by_tags(
            tags=self.request.GET.getlist('tags'),
        )
        return queryset


class RecipeDetailView(DetailView):
    """Страница отдельного рецепта."""

    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/singlePage.html'


class ProfileView(PaginatorRedirectMixin, ListView):
    """Страница рецептов отдельного автора."""

    context_object_name = 'author_recipes'
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/authorRecipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterform'] = FilterForm(self.request.GET)
        context['author'] = get_object_or_404(User, id=self.kwargs.get('id'))
        return context

    def get_queryset(self):
        queryset = services.get_recipes_queryset_filtered_by_tags(
            user_id=self.kwargs.get('id'),
            tags=self.request.GET.getlist('tags'),
        )
        return queryset


class SubscriptionsView(LoginRequiredMixin, PaginatorRedirectMixin, ListView):
    """Список авторов, на которых подписан пользователь."""

    context_object_name = 'authors'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/myFollow.html'

    def get_queryset(self):
        queryset = services.get_user_subscriptions_list(
            user_id=self.request.user.id
        )
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterform'] = FilterForm(self.request.GET)
        context['req_args'] = self.request.GET.getlist('tags')
        return context

    def get_queryset(self):
        queryset = services.get_recipes_queryset_filtered_by_tags(
            user_id=self.request.user.id,
            model=Favorite,
            tags=self.request.GET.getlist('tags'),
        )
        return queryset


class PurchasesView(LoginRequiredMixin, ListView):
    """Список покупок пользователя."""

    context_object_name = 'purchases'
    ordering = '-pub_date'
    template_name = 'recipes/purchaseList.html'

    def get_queryset(self):
        queryset = services.get_recipes_queryset_filtered_by_tags(
            user_id=self.request.user.id,
            model=Purchase,
        )
        return queryset


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
