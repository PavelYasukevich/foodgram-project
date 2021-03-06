from rest_framework import serializers

from .models import Ingredient, Purchase, Subscription


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Subscription


class IngredientSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    dimension = serializers.CharField(source='measurement_unit')

    class Meta:
        fields = '__all__'
        model = Ingredient