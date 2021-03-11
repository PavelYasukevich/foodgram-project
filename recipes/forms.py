from django import forms

from .models import Amount, Ingredient, Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'description', 'image']
