import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


def read_ingredients():
    with open(os.path.join(settings.BASE_DIR, 'data', 'ingredients.json'),
              'r', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(len(data)):
            Ingredient.objects.get_or_create(
                name=data[i].get("name"),
                measurement_unit=data[i].get("measurement_unit")
            )


class Command(BaseCommand):

    def handle(self, *args, **options):
        read_ingredients()
