from django.shortcuts import render

# Импортируем модель, чтобы обратиться к ней
from .models import Recipes


def index(request):
    recipes = Recipes.objects.order_by('-pub_date')[:10]
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)
