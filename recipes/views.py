from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django_pdfkit import PDFView
from pytils.translit import slugify
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .forms import FilterForm, RecipeForm
from .models import Amount, Ingredient, Purchase, Recipe, Tag
from .serializers import (
    FavoritesSerializer,
    IngredientSerializer,
    PurchaseSerializer,
    SubscriptionsSerializer,
)

User = get_user_model()


class IndexView(ListView):
    context_object_name = 'recipes'
    model = Recipe
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterform'] = FilterForm(self.request.GET)
        context['req_args'] = self.request.GET.getlist('tags')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.GET.getlist('tags')
        if tags:
            for tag in tags:
                queryset = queryset.filter(tags__name__contains=tag)
        return queryset


class RecipeDetailView(DetailView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/singlePage.html'


class ProfileView(ListView):
    context_object_name = 'author_recipes'
    model = Recipe
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/authorRecipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterform'] = FilterForm(self.request.GET)
        context['author'] = get_object_or_404(User, id=self.kwargs.get('id'))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('id'))
        queryset = super().get_queryset().filter(author=user)
        tags = self.request.GET.getlist('tags')
        if tags:
            for tag in tags:
                queryset = queryset.filter(tags__name__contains=tag)
        return queryset


class SubscriptionsView(ListView):
    context_object_name = 'authors'
    model = User
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/myFollow.html'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = super().get_queryset().filter(subscribers__user__id=user.id)
        return queryset


class CreateDestroyViewset(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin
):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True}, status=status.HTTP_200_OK)


class SubscriptionsViewSet(CreateDestroyViewset):
    serializer_class = SubscriptionsSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset, author__id=self.kwargs[self.lookup_field]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'user': request.user.id,
                'author': request.data['id'],
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


def create_new_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    tags = Tag.objects.all()
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.slug = slugify(new_recipe.name)
        new_recipe.save()

        for tag_name, _ in Tag.CHOICES:
            if request.POST.get(tag_name) is not None:
                tag_to_add = get_object_or_404(Tag, name=tag_name)
                new_recipe.tags.add(tag_to_add)

        for name, value in request.POST.items():
            if name.startswith('nameIngredient_'):
                num = int(name.split('_')[1])
                ingr_to_add = get_object_or_404(Ingredient, name=value)
                amount_value = int(request.POST.get(f'valueIngredient_{num}'))
                Amount.objects.create(
                    value=amount_value,
                    recipe=new_recipe,
                    ingredient=ingr_to_add,
                )
                new_recipe.ingredients.add(ingr_to_add)
        return redirect('index')

    return render(request, 'recipes/formRecipe.html', {'form': form, 'tags': tags})


class UpdateRecipeView(UpdateView):
    context_object_name = 'recipe'
    extra_context = {'tags': Tag.objects.all()}
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'
    queryset = Recipe.objects.all()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        new_tags = []
        for tag_name, _ in Tag.CHOICES:
            if self.request.POST.get(tag_name) is not None:
                tag_to_add = get_object_or_404(Tag, name=tag_name)
                new_tags.append(tag_to_add)
        self.object.tags.set(new_tags)

        new_ingrs = []
        for name, value in self.request.POST.items():
            if name.startswith('nameIngredient_'):
                num = int(name.split('_')[1])
                ingr_to_add = get_object_or_404(Ingredient, name=value)
                amount_value = int(
                    self.request.POST.get(f'valueIngredient_{num}')
                )
                new_ingrs.append((ingr_to_add, amount_value))

        Amount.objects.filter(recipe=self.object).delete()
        for ingr, amount_value in new_ingrs:
            Amount.objects.create(
                value=amount_value, recipe=self.object, ingredient=ingr
            )
            self.object.ingredients.add(ingr)

        self.object.save()
        return redirect(self.get_success_url())


class FavoritesView(ListView):
    context_object_name = 'favorites'
    model = Recipe
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/favorite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterform'] = FilterForm(self.request.GET)
        context['req_args'] = self.request.GET.getlist('tags')
        return context

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        user_favs = user.favorites.values_list('recipe__id', flat=True)
        queryset = super().get_queryset().filter(id__in=user_favs)
        tags = self.request.GET.getlist('tags')
        if tags:
            for tag in tags:
                queryset = queryset.filter(tags__name__contains=tag)
        return queryset


class PurchasesView(ListView):
    context_object_name = 'purchases'
    model = Recipe
    ordering = '-pub_date'
    paginate_by = settings.OBJECTS_PER_PAGE
    template_name = 'recipes/purchaseList.html'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        user_purchases = user.purchases.values_list('recipe__id', flat=True)
        queryset = super().get_queryset().filter(id__in=user_purchases)
        return queryset


class DownloadShoppingList(PDFView):
    template_name = 'recipes/aux/shopping_list.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        purchase_list = {}
        purchases = self.request.user.purchases.select_related('recipe').all()
        for purchase in purchases:
            ingredients = purchase.recipe.ingredients.all()
            for ingr in ingredients:
                amount = Amount.objects.get(recipe=purchase.recipe, ingredient=ingr).value
                purchase_list[ingr] = purchase_list.get(ingr, 0) + amount

        kwargs.update(
            {'purchase_list': purchase_list}
        )
        return kwargs


class IngredientsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(name__startswith=query)
        return queryset


class FavoritesViewSet(CreateDestroyViewset):
    serializer_class = FavoritesSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset, recipe__id=self.kwargs[self.lookup_field]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.favorites.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'user': request.user.id,
                'recipe': request.data['id'],
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class DeleteRecipeView(DeleteView):
    model = Recipe
    template_name = 'recipes/deleteRecipe.html'
    success_url = reverse_lazy('index')


class PurchasesViewSet(CreateDestroyViewset):
    serializer_class = PurchaseSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset, recipe__id=self.kwargs[self.lookup_field]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.purchases.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'user': request.user.id,
                'recipe': request.data['id'],
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
