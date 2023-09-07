from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Follow, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag, User)
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


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
        if not request:
            return False
        return obj.following.filter(user=request.user.id).exists()

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


class SubscribedSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Подписок. """
    recipe = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Ингредиенты. """
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Теги. """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор для связи модели Рецепты/Ингридиенты. """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    units_of_measurement = serializers.ReadOnlyField(
                           source='ingredient.units_of_measurement')

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'units_of_measurement',
            'amount_of_ingredient'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Рецепты. """
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(many=True, read_only=True,
                                             source='ingredientrecipe_set')
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
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        """ Наличие рецепта в списке покупок. """
        request = self.context.get('request')
        if not request:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user.id).exists()


#    class RecipeCreateSerializer(serializers.ModelSerializer):
#   """ Сериализатор для добавления рецепта. """


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Списка покупок """
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        # нужно сделать отображение в списке покупок


class FavoriteSerializer(serializers.ModelSerializer):
    """ Сериализатор модели избранных рецептов """
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(),
                                                write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              write_only=True)

    class Meta:
        model = Favorite
        fields = ('user',
                  'recipe')
        # нужно сделать отображение добавленного в избр


class FollowSerializer(serializers.ModelSerializer):
    """ Сериализатор модели подписок """
    user = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = '__all__'
