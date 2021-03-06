from django import forms

from .models import Amount, Ingredient, Recipe, TAG_CHOICES


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ["name", "cooking_time", "description", "image"]
