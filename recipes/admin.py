from django.contrib import admin

from .models import (Amount, Favorite, Ingredient, Purchase, Recipe,
                     Subscription, Tag)


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'value')
    list_filter = ('recipe',)
    ordering = ('recipe',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass


class AmountInline(admin.TabularInline):
    model = Amount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'name', 'tags', 'cooking_time', 'author', 'description',
        'slug', 'image', 'fav_counter', 'pub_date'
    )
    inlines = [AmountInline]
    list_display = (
        'id',
        'name',
        'author',
    )
    list_display_links = ('name',)
    list_filter = (
        'author',
        'name',
        'tags',
    )
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('fav_counter', 'pub_date')




@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('name',)
