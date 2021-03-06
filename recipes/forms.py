from django import forms

from .models import Amount, Ingredient, Recipe, TAG_CHOICES


class RecipeForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(choices=TAG_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Recipe
        fields = ["name", "tags", "cooking_time", "description", "image"]


class AmountForm(forms.ModelForm):
    class Meta:
        model = Amount
        fields = ["ingredient", "value"]


AmountFormSet = forms.formset_factory(AmountForm, can_delete=True)