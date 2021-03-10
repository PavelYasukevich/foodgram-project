from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()
TAG_CHOICES = [('zv', 'Завтрак'), ('ob', 'Обед'), ('uz', 'Ужин')]

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта',
    )
    name = models.CharField(
        max_length=100,
        help_text='Название рецепта, 100 символов',
        verbose_name='Название',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Изображение',
        upload_to='recipes/',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='Amount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
        help_text='Ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Тэги',
        help_text='Тэги рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации',
    )
    fav_counter = models.PositiveSmallIntegerField(
        verbose_name='Добавлений в избранное',
        help_text='Счетчик добавлений в избранное',
        default=0,
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.name}, автор: {self.author}'

    def get_absolute_url(self):
        return reverse('recipe', args=[self.slug])


class Ingredient(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        verbose_name='Название ингредиента',
        help_text='Название ингредиента, 100 символов'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Единица измерения',
    )

    def __str__(self):
        return self.name


class Amount(models.Model):
    value = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Количество ингредиента, необходимое для рецепта',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingr'
            )
        ]

    def __str__(self):
        rec = Recipe.objects.get(id=self.recipe.id)
        ingr = Ingredient.objects.get(id=self.ingredient.id)
        unit = ingr.measurement_unit
        return f'{self.value} {unit} {ingr} для {rec.name}'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase',
            )
        ]

    def __str__(self):
        return f'Ингридиенты для {self.recipe}'


class Tag(models.Model):
    name = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Тег',
        help_text='Тег',
        choices=TAG_CHOICES,
    )

    def __str__(self):
        return self.get_name_display()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE,
        verbose_name='Автор, на которого подписаны',
        help_text='Автор, на которого подписаны',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription',
            )
        ]

    def __str__(self):
        return f'{self.user.username} subscribed on {self.author.username}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_fav'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'
