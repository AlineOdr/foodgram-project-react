from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password']
    username = models.CharField(
        unique=True,
        max_length=150,
    )
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=254, blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=254, blank=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=254, blank=False
    )


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(max_length=200)
#    quantity = models.PositiveIntegerField()
    units_of_measurement = models.TextField(
        max_length=200,
        verbose_name=('Единица измерения')
        )

    class Meta:
        verbose_name = ('Ингредиент')
        verbose_name_plural = ('Ингредиенты')


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(max_length=200)
    colour = models.CharField(
        max_length=200,
        verbose_name=('Цвет')
        )
    slug = models.SlugField(max_length=255,
                            unique=True)

    class Meta:
        verbose_name = ('Тег')
        verbose_name_plural = ('Теги')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        null=True
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipe/',
        blank=True
    )
    text = models.TextField(verbose_name=('Описание'))
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name=('Теги')
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name=('Ингредиенты'),
    )
    cooking_time = models.PositiveIntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = ('Рецепт')
        verbose_name_plural = ('Рецепты')

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    """Модель ингредиентов, связанных с рецептами."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount_of_ingredient = models.PositiveIntegerField(
        verbose_name=('Количество ингредиента')
    )

    class Meta:
        verbose_name = ('Ингредиент, связанный с рецептом')
        verbose_name_plural = ('Ингредиенты, связанные с рецептами')


class TagRecipe(models.Model):
    """Модель ингредиентов, связанных с рецептами."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ('Тег, связанный с рецептом')
        verbose_name_plural = ('Теги, связанные с рецептами')


class ShoppingCart(models.Model):
    """Модель списка покупок по рецепту."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
        null=True,
        verbose_name=('Покупатель')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes',
        verbose_name=('Рецепт')
    )

    class Meta:
        verbose_name = ('Список покупок')
        verbose_name_plural = ('Списки покупок')


class Favorite(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name=('Пользователь')
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name=('Рецепт в избранном')
    )

    class Meta:
        verbose_name = ('Избранное')
        verbose_name_plural = ('Избранные')


class Follow(models.Model):
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
        verbose_name = ('Подписчик')
        verbose_name_plural = ('Подписчики')
        constraints = [models.CheckConstraint(
            check=~models.Q(author=models.F('user')),
            name='cannot subscribe to yourself'),
            models.UniqueConstraint(name='unique_subscribe',
                                    fields=['user', 'author'],)]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
