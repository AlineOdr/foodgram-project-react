# Generated by Django 3.2 on 2023-10-02 11:21

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20231002_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(choices=[('#25D315', 'Зеленый'), ('#D31D20', 'Красный'), ('#5CD3BB', 'Голубой')], default='#FFFFFF', error_messages={'unique': 'Тег с таким цветом уже существует!'}, image_field=None, max_length=25, samples=None, unique=True, verbose_name='Цвет(HEX-код)'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(error_messages={'unique': 'Тег с таким названием уже существует!'}, max_length=200, unique=True, verbose_name='Название'),
        ),
    ]
