from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        verbose_name='Избранные рецепты',
        help_text='Избранные рецепты',
    )
