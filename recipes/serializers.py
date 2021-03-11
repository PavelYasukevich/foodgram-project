from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Favorite, Ingredient, Purchase, Subscription

User = get_user_model()


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Subscription


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Favorite


class IngredientSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    dimension = serializers.CharField(source='measurement_unit')

    class Meta:
        fields = '__all__'
        model = Ingredient


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Purchase
