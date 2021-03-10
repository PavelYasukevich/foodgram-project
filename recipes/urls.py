from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
# router.register(r'purchases', PurchasesViewSet)
router.register('subscriptions', views.SubscriptionsViewSet, basename='subscriptions')
router.register('favorites', views.FavoritesViewSet, basename='favorites')
router.register('ingredients', views.IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('api/', include(router.urls)),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('recipe/new/', views.create_new_recipe, name='new_recipe'),
    path('recipe/<slug:slug>/', views.RecipeDetailView.as_view(), name='recipe'),
    path('recipe/<slug:slug>/edit/', views.UpdateRecipeView.as_view(), name='edit_recipe'),
    path('recipe/<slug:slug>/delete/', views.DeleteRecipeView.as_view(), name='delete_recipe'),
    path('subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('purchases/', views.PurchasesView.as_view(), name='purchases'),
    path('', views.IndexView.as_view(), name='index'),

]
