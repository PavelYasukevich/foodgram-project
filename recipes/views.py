from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import mixins, viewsets


from .models import Amount, Ingredient, Purchase, Recipe, Subscription, Tag
from .serializers import SubscriptionsSerializer


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
    lookup_field = 'id'
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=self.kwargs.get('id'))
        user= self.request.user
        serializer = self.get_serializer(data={'user': user.id, 'author': author.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

