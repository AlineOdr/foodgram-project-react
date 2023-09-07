from django.shortcuts import render

# Импортируем модель, чтобы обратиться к ней
from .models import Recipe

def index(request):
    recipes = Recipe.objects.order_by('-pub_date')[:10]
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)
