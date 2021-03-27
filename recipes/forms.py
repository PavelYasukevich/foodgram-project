from django import forms
from django.core.exceptions import ValidationError

from pytils.translit import slugify

from .models import Amount, Ingredient, Recipe


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

    def __init__(self, request, ingredients=None, **kwargs):
        super().__init__(**kwargs)
        self.request = request
        if ingredients is not None:
            self.ingredients = [
                (
                    ingredient.name,
                    ingredient.amount,
                    ingredient.measurement_unit
                )
                for ingredient
                in ingredients
            ]

    def save(self, commit=True):
        self.instance = super().save(commit=False)
        self.instance.author = self.request.user
        self.instance.slug = slugify(self.instance.name)
        self.instance.save()

        Amount.objects.filter(recipe=self.instance).delete()

        for name, amount, _ in self.ingredients:
            ingredient = Ingredient.objects.get(name=name)
            Amount.objects.create(
                value=amount,
                recipe=self.instance,
                ingredient=ingredient
            )
            self.instance.ingredients.add(ingredient)

        self.save_m2m()
        return self.instance

    def clean(self):
        super().clean()
        ingredients = dict()
        for html_name, ingredient_name in self.data.items():
            if html_name.startswith('nameIngredient_'):
                number_at_the_end = int(html_name.split('_')[1])
                ingredients[ingredient_name] = ingredients.get(
                    ingredient_name, 0) + int(
                    self.data.get(f'valueIngredient_{number_at_the_end}')
                )
        valid_ingredients = Ingredient.objects.filter(name__in=ingredients)
        form_ingredients = [
            (
                ingredient.name,
                ingredients[ingredient.name],
                ingredient.measurement_unit
            )
            for ingredient
            in valid_ingredients
            if ingredients[ingredient.name] > 0
        ]

        self.ingredients = form_ingredients

        if valid_ingredients.count() != len(ingredients):
            raise ValidationError('Пожалуйста, выбирайте только из списка '
                                  'существующих ингредиентов.')

        for amount in ingredients.values():
            if not isinstance(amount, int) or amount < 0:
                raise ValidationError('Количество ингредиента должно быть '
                                      'целым положительным числом')

        if not ingredients:
            raise ValidationError('Не указано ни одного ингредиента '
                                  'из существующего перечня')
