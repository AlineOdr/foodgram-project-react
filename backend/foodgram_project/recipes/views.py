from django.shortcuts import render
# Импортируем модель, чтобы обратиться к ней
from .models import Recipes

def index(request):
    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию (от больших значений к меньшим)
    pecipes = Recipes.objects.order_by('-pub_date')[:10]
    # В словаре context отправляем информацию в шаблон
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)
