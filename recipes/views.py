from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .forms import AmountFormSet, RecipeForm
from .models import Amount, Ingredient, Purchase, Recipe, Subscription, Tag
from .serializers import IngredientSerializer, SubscriptionsSerializer


User = get_user_model()

class IndexView(ListView):
    context_object_name = 'recipes'
    model = Recipe
    template_name = 'recipes/index.html'
    # ordering 
    # paginator_class


class RecipeDetailView(DetailView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/singlePage.html'



class ProfileView(DetailView):
    context_object_name = 'author'
    model = User
    template_name = 'recipes/authorRecipe.html'
        

class SubscriptionsView(ListView):
    context_object_name = 'authors'
    template_name = 'recipes/myFollow.html'
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = User.objects.filter(subscribers__user__id=user.id)
        return queryset


class CreateDestroyViewset(viewsets.GenericViewSet, 
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin
                            ):
    """Proxy class"""
    pass


class SubscriptionsViewSet(CreateDestroyViewset):
    serializer_class = SubscriptionsSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, author__id=self.kwargs[self.lookup_field])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    def create(self, request, *args, **kwargs):
        user= self.request.user
        serializer = self.get_serializer(data={'user': user.id, 'author': self.request.data['id']})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class NewRecipeView(CreateView):
#     # fields = '__all__'
#     form_class = RecipeForm
#     model = Recipe
#     template_name = 'recipes/newRecipe.html'


def create_new_recipe(request):
    recipe_form = RecipeForm(request.POST or None)
    amount_formset = AmountFormSet(
        request.POST or {
            'amount-TOTAL_FORMS': '1',
            'amount-INITIAL_FORMS': '1',
        },
        prefix="amount"
    )
    if recipe_form.is_valid() and amount_formset.is_valid():
        return redirect('index')
    else:
        for error in recipe_form.errors:
            print(error)
    return render(
        request,
        'recipes/newRecipe.html',
        {'recipe_form': recipe_form, 'amount_formset': amount_formset}
    )


class FavoritesView(ListView):
    model = Recipe
    template_name = 'recipes/favorite.html'


class PurchasesView(ListView):
    model = Purchase
    template_name = 'recipes/purchaseList.html'


class IngredientsViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin):
    
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(name__startswith=query)
        return queryset