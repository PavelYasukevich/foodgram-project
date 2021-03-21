from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Ingredient

from .serializers import (FavoritesSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionsSerializer)


class CreateDestroyViewset(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'success': True}, status=status.HTTP_200_OK)


class FavoritesViewSet(CreateDestroyViewset):
    serializer_class = FavoritesSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset, recipe__id=self.kwargs[self.lookup_field]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.favorites.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'user': request.user.id,
                'recipe': request.data['id'],
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class IngredientsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(name__startswith=query)
        return queryset


class PurchasesViewSet(CreateDestroyViewset):
    serializer_class = PurchaseSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset, recipe__id=self.kwargs[self.lookup_field]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.purchases.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'user': request.user.id,
                'recipe': request.data['id'],
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SubscriptionsViewSet(CreateDestroyViewset):
    serializer_class = SubscriptionsSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset, author__id=self.kwargs[self.lookup_field]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'user': request.user.id,
                'author': request.data['id'],
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
