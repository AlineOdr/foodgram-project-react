# Generated by Django 3.2 on 2023-10-03 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20231003_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to='recipes.recipe', verbose_name='Рецепт в избранном'),
        ),
    ]
