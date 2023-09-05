import csv
import settings

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Transserfing from csv to database'
    def handle(self, *args, **options):
        for model, file in Ingredient.items():
        with open(settings.BASE_DIR/data/ingredients, encoding='utf-8') as file:
                if csv_file != 'users.csv':
                    reader = csv.reader(file)
                    for row in reader:
                        Ingredient.objects.create(
                            name=row['name'],
                            units_of_measurement=row['units_of_measurement'],)

