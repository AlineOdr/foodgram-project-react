from drf_extra_fields.fields import Base64ImageField
from recipes.models import (  # TagRecipe,
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

#    from rest_framework.validators import UniqueTogetherValidator

#   делаю как ниже, но в action вылетает ошмбка isort (проходит только
#    как выше)
#    from drf_extra_fields.fields import Base64ImageField
#
#    from rest_framework import serializers
#    from rest_framework.fields import SerializerMethodField
#
#    from recipes.models import (Favorite, Follow, Ingredient,
#                IngredientRecipe, Recipe, ShoppingCart, Tag, User)


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для пользователей . """
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and Follow.objects.filter(
            user=request.user,
            author=obj).exists()

    def create(self, validated_data):
        """Создание нового пользователя"""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Рецепты. """

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Списка покупок """
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)

    class Meta:
        model = ShoppingCart
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Ингредиенты. """
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "units_of_measurement"
        )


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Теги. """

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "colour",
            "slug"
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор для связи модели Рецепты/Ингридиенты. """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    units_of_measurement = serializers.ReadOnlyField(
        source='ingredient.units_of_measurement'
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'units_of_measurement',
            'amount'
        )
#        validators = [
#            UniqueTogetherValidator(
#                queryset=IngredientRecipe.objects.all(),
#                fields=('ingredient', 'recipe')
#            )
#        ]


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Рецепты. """
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(many=True, read_only=True,
                                             source='recipe_ingredients')
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
            "cooking_time"
        )

    def get_is_favorited(self, obj):
        """ Наличие рецепта в избранном. """
        request = self.context.get('request')
        return request.user.is_authenticated and Favorite.objects.filter(
            recipe=obj,
            user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        """ Наличие рецепта в списке покупок. """
        request = self.context.get('request')
        return request.user.is_authenticated and ShoppingCart.objects.filter(
            recipe=obj,
            user=request.user.id).exists()

    def validate_ingredients(self, ingredients):
        """Проверка ингредиентов."""
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо указать ингредиент!'
            )

        for ingredient in ingredients:
            amount = ingredient.get('amount')
            ingredient = ingredient.get('ingredient')
            ingredient_tuple = (ingredient.id, amount)
            ingredients_set = set()
            if ingredient_tuple in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент не может повторяться!'
                )
            ingredients_set.add(ingredient_tuple)
        return ingredients

    def validate_tags(self, tags):
        """Проверка тэгов."""
        if not tags:
            raise serializers.ValidationError(
                'Необходимо указать тэг!'
            )

        for tag in tags:
            try:
                Tag.objects.get(id=tag.id)
            except Tag.DoesNotExist:
                raise serializers.ValidationError(
                    'Тег не может повторяться!'
                )
        return tags


class CreateRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Рецепты (Создание). """
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), source='tag')
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='recipe_ingredients')

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "pub_date"
            "author",
            "image",
            "name",
            "text",
            "cooking_time"
        )

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientRecipe.objects.bulk_create([
                IngredientRecipe(recipe=recipe,
                                 ingredient=ingredient,
                                 amount=ingredient.get(
                                    'amount'))]
                                )

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(tags)
#        for ingredient in ingredients:
#            current_ingredient, status = Ingredient.objects.get_or_create(
#                **ingredient
#            )
#            IngredientRecipe.objects.create(
#                ingredient=current_ingredient, recipe=recipe
#            )
#        for tag in tags:
#            current_tag, status = Tag.objects.get_or_create(
#                **tag
#            )
#            TagRecipe.objects.create(
#                tag=current_tag, recipe=recipe
#            )
        self.create_ingredients(ingredients, recipe)
        return recipe


class FavoriteSerializer(serializers.ModelSerializer):
    """ Сериализатор модели избранных рецептов """
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)

    class Meta:
        model = Favorite
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


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
            'recipes_count'
        )
#        validators = (validators.UniqueTogetherValidator(
#                    queryset=Follow.objects.all(),
#                    fields=('user', 'author',),
#                    message='Нельзя подписываться дважды на одного автора!'
#                    ),)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and Follow.objects.filter(
            user=request.user,
            author=obj).exists()
#    def create(self, validated_data):
#        user = self.context['user']
#        author = self.context['author']
#        Follow.objects.create(user=user, author=author)
#        return author

#    def validate(self, data):
#        if self.context.get('request').user == data['author']:
#            raise serializers.ValidationError(
#                'Вы не можете быть подписаны на самого себя!')
#        return data

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSubscribeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipe.count()
#        validators = (validators.UniqueTogetherValidator(
#                      queryset=Follow.objects.all(),
#                      fields=('user', 'following',),
#                      message='Нельзя подписываться дважды на одного автора!'
#                      ),)
