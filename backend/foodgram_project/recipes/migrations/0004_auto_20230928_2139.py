# Generated by Django 3.2 on 2023-09-28 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230928_2107'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='Нельзя рецепт добавить дважды в избранное',
        ),
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_favorite',
        ),
    ]