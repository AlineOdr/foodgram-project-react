#    import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_color


class User(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password',
    )
    username = models.CharField(
        'Имя пользователя',
        unique=True,
        max_length=150,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=254
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=254
    )
    password = models.CharField(
        'Пароль',
        max_length=254
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название',
        max_length=200)
    units_of_measurement = models.TextField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.units_of_measurement}'


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    colour = models.CharField(
        'Цвет(HEX-код)',
        validators=[validate_color],
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=255,
        unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название',
        max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipe/'
    )
    text = models.TextField('Описание')
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(1, 'Значение не может равняться 0.'),
            MaxValueValidator(1440, 'Значение должно быть меньше 1440.'),
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        blank=True,
        null=True,
        #        default=datetime.date.today
        )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    """Модель ингредиентов, связанных с рецептами."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipes_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        default=1,
        validators=(
            MinValueValidator(1, 'Значение не может равняться 0.'),
            MaxValueValidator(100, 'Значение должно быть меньше 100.'),
        )

    )

    class Meta:
        verbose_name = 'Ингредиент, связанный с рецептом'
        verbose_name_plural = 'Ингредиенты, связанные с рецептами'

    def __str__(self):
        return self.ingredient.name


class TagRecipe(models.Model):
    """Модель ингредиентов, связанных с рецептами."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тэг',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Тэг, связанный с рецептом'
        verbose_name_plural = 'Теги, связанные с рецептами'


class ShoppingCart(models.Model):
    """Модель списка покупок по рецепту."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Favorite(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепт в избранном'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Follow(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [models.CheckConstraint(
            check=~models.Q(author=models.F('user')),
            name='cannot subscribe to yourself'),
            models.UniqueConstraint(name='unique_subscribe',
                                    fields=['user', 'author'],)]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
