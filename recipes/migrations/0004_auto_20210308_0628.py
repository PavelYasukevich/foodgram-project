# Generated by Django 3.1.7 on 2021-03-08 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210304_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='fav_counter',
            field=models.PositiveSmallIntegerField(default=0, help_text='Счетчик добавлений в избранное', verbose_name='Добавлений в избранное'),
        ),
    ]
