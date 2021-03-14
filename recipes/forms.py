from django import forms

from .models import Amount, Ingredient, Recipe, Tag


class ImageFieldWidget(forms.ClearableFileInput):
    template_name = 'recipes/aux/imagefield_widget.html'


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'description', 'image']
        widgets = {
            'image': ImageFieldWidget(),
        }


class FilterForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name='name',
        widget=forms.CheckboxSelectMultiple,
    )
