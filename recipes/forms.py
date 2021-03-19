from django import forms

from .models import Recipe, Tag


class ImageFieldWidget(forms.ClearableFileInput):
    template_name = 'recipes/aux/imagefield_widget.html'


class SpecialCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = 'recipes/aux/tag_checkbox_option.html'


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'description', 'image', 'tags']
        widgets = {
            'image': ImageFieldWidget(),
            'tags': SpecialCheckboxSelectMultiple(),
        }


class FilterForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name='name',
        widget=forms.CheckboxSelectMultiple,
    )
