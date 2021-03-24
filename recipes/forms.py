from django import forms
from pytils.translit import slugify

from .models import Recipe


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

    def __init__(self, request, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        self.instance.author = self.request.user
        self.instance.slug = slugify(self.instance.name)
        self.instance.save()
        self.save_m2m()
        return self.instance
