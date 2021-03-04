from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import Amount, Ingredient, Purchase, Recipe, Subscription, Tag


User = get_user_model()

class IndexView(ListView):
    model = Recipe
    # ordering 
    # paginator_class

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'recipes/indexAuth.html'
        else:
            return 'recipes/indexNotAuth.html'


class RecipeDetailView(DetailView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/singlePage.html'



class ProfileView(DetailView):
    model = User
    template_name = 'recipes/authorRecipe.html'
        

class SubscriptionsView(ListView):
    template_name = 'recipes/myFollow.html'
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        return user.subscriptions