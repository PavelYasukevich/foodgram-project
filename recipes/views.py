from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import Amount, Ingredient, Purchase, Recipe, Subscription, Tag


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
    model = Recipe