from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import Amount, Ingredient, Purchase, Recipe, Subscription, Tag


User = get_user_model()

class IndexView(ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    # ordering 
    # paginator_class


class RecipeDetailView(DetailView):
    context_object_name = 'recipe'
    model = Recipe
    template_name = 'recipes/singlePage.html'



class ProfileView(DetailView):
    model = User
    template_name = 'recipes/authorRecipe.html'
        

class SubscriptionsView(ListView):
    context_object_name = 'authors'
    template_name = 'recipes/myFollow.html'
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = User.objects.filter(subscribers__user__id=user.id)
        return queryset