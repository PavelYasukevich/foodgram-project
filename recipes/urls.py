from django.urls import path

from . import views


urlpatterns = [
    path('<int:id>/profile/', views.ProfileView.as_view(), name='profile'),
    path('recipe/new/', views.CreateRecipeView.as_view(), name='new_recipe'),
    path(
        'recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe'
    ),
    path(
        'recipe/<int:pk>/edit/',
        views.UpdateRecipeView.as_view(),
        name='edit_recipe',
    ),
    path(
        'recipe/<int:pk>/delete/',
        views.DeleteRecipeView.as_view(),
        name='delete_recipe',
    ),
    path(
        'subscriptions/',
        views.SubscriptionsView.as_view(),
        name='subscriptions',
    ),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('purchases/', views.PurchasesView.as_view(), name='purchases'),
    path('download/', views.DownloadShoppingList.as_view(), name='download'),
    path('', views.IndexView.as_view(), name='index'),
]
