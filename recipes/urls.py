from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('profile/<str:username>/', name='profile'),
    path('recipe/<slug:slug>/', views.RecipeDetailView.as_view(), name='recipe'),
    # path('recipe/<slug:slug>/new/', name='new_recipe'),
    # path('recipe/<slug:slug>/edit/', name='edit_recipe'),
    # path('subscriptions/', name='subscriptions'),
    # path('favorites/', name='favorites'),
    # path('purchases/', name='purchases'),
]
