from rest_framework import serializers

from .models import Ingredient, Purchase, Subscription


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Subscription
