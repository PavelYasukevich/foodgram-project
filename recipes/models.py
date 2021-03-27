from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class RecipeQuerySet(models.QuerySet):
    def annotated(self, user):
        queryset = self
        if user.is_authenticated:
            in_purchases = Purchase.objects.filter(
                recipe=models.OuterRef('pk'),
                user=user
            )
            in_favorites = Favorite.objects.filter(
                recipe=models.OuterRef('pk'),
                user=user
            )
            in_subs = Subscription.objects.filter(
                author=models.OuterRef('author'),
                user=user
            )
            queryset = queryset.annotate(
                in_favored=models.Exists(in_favorites),
                in_purchased=models.Exists(in_purchases),
                in_subscriptions=models.Exists(in_subs)
            )

        queryset = queryset.prefetch_related(
            models.Prefetch(
                'ingredients',
                queryset=(
                    Ingredient.objects.distinct().annotate(
                        amount=models.Subquery(
                            Amount.objects.filter(
                                ingredient=models.OuterRef('pk'),
                                recipe=models.OuterRef('recipe__id'),
                            ).values('value')[:1],
                        )
                    )
                )
            )
        )
        
        return queryset


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
        help_text='Размер файла не более 5Мб',
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
    slug = models.SlugField(
        max_length=100,
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}, автор: {self.author}'

    def get_absolute_url(self):
        return reverse('recipe', args=[self.pk])

    def added_in_favorites(self):
        return self.favorites.count()

    added_in_favorites.short_description = 'Добавлений в избранное'
    fav_counter = property(added_in_favorites)


class Ingredient(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        verbose_name='Название ингредиента',
        help_text='Название ингредиента, 100 символов',
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

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
        related_name='amounts',
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )

    class Meta:
        verbose_name = 'Количество'
        verbose_name_plural = 'Количества'

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_ingr'
            )
        ]

    def __str__(self):
        rec = self.recipe
        ingr = self.ingredient
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
        related_name='purchased',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase',
            )
        ]

    def __str__(self):
        return f'Ингридиенты для {self.recipe}'


class Tag(models.Model):
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин'),
    ]

    name = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Тег',
        help_text='Тег',
        choices=CHOICES,
    )
    color = models.CharField(
        max_length=10,
        verbose_name='Цвет',
        help_text='Цвет тега на страницах сайта',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(user__exact=models.F('author')),
                name='self_sub_inhibit'
            )
        ]

    def __str__(self):
        return f'{self.user} subscribed on {self.author}'


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
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='unique_fav'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'
