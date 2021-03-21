from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('purchases', views.PurchasesViewSet, basename='purchases')
router.register(
    'subscriptions', views.SubscriptionsViewSet, basename='subscriptions'
)
router.register('favorites', views.FavoritesViewSet, basename='favorites')
router.register(
    'ingredients', views.IngredientsViewSet, basename='ingredients'
)

urlpatterns = [
    path('', include(router.urls)),
]
