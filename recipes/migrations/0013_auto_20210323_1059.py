# Generated by Django 3.1.7 on 2021-03-23 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='Цвет тега на страницах сайта', max_length=10, unique=True, verbose_name='Цвет'),
        ),
    ]
