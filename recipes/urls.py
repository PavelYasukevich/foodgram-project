from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register(r'purchases', PurchasesViewSet)
router.register(r'subscriptions', views.SubscriptionsViewSet, basename='subscriptions')
# router.register(r'favorites', FavoritesViewSet)
# router.register(r'ingredients', IngredientsViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('recipe/<slug:slug>/', views.RecipeDetailView.as_view(), name='recipe'),
    # path('recipe/<slug:slug>/new/', name='new_recipe'),
    # path('recipe/<slug:slug>/edit/', name='edit_recipe'),
    path('subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions'),
    # path('favorites/', name='favorites'),
    # path('purchases/', name='purchases'),
    path('', views.IndexView.as_view(), name='index'),

]
