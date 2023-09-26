import re

from rest_framework.exceptions import ValidationError


def validate_color(value):
    """Проверяет, что строка 'Цвет' соответствует кодировке цвета HEX."""

    hexColor = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    if not re.match(hexColor, value):
        raise ValidationError('Некорректный формат HEX-цвета')
