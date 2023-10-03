from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    User,
)
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей ."""

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Follow.objects.filter(user=request.user, author=obj).exists()
        )

    def create(self, validated_data):
        """Создание нового пользователя"""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепты."""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор модели Списка покупок"""

    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ("id", "name", "image", "cooking_time")


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ингредиенты."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Теги."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для связи модели Рецепты/Ингридиенты."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепты (Чтение)."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='recipes_ingredients',
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        """Наличие рецепта в избранном."""
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(recipe=obj, user=request.user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Наличие рецепта в списке покупок."""
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and ShoppingCart.objects.filter(
                recipe=obj, user=request.user.id
            ).exists()
        )


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для связи модели Рецепты с Ингредиенты (Запись)."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепты (Создание)."""

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    author = UserSerializer(read_only=True,
                            default=serializers.CurrentUserDefault())
    image = Base64ImageField()
    ingredients = RecipeIngredientWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=['author', 'name'],
                message='Такой рецепт уже существует!')
        ]
        read_only_fields = ("id", "author",)

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get("ingredients")
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Ингредиент не может повторяться!'
            )
        if not ingredients:
            raise serializers.ValidationError('Необходимо указать ингредиент!')
        return data

    def validate_tags(self, tags):
        """Проверка тэгов."""
        if not tags:
            raise serializers.ValidationError('Необходимо указать тэг!')

        #        for tag in tags:
        #            try:
        #                Tag.objects.get(id=tag.id)
        #            except Tag.DoesNotExist:
        #                raise serializers.ValidationError('Тег не может повторяться!')
        #        return tags

    def create_ingredients(self, recipe, ingredients):
        IngredientRecipe.objects.bulk_create(
            IngredientRecipe(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags_data = validated_data.pop('tags', None)
        instance.tags.clear()
        instance.tags.add(*tags_data)
        instance.ingredients.clear()
        self.create_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели избранных рецептов"""

    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )

    class Meta:
        model = Favorite
        fields = ("id", "name", "image", "cooking_time")


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Follow.objects.filter(user=request.user, author=obj).exists()
        )

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = recipes[: int(limit)]
        serializer = RecipeSubscribeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipe.count()
