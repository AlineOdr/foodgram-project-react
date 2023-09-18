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
        user = self.context.get('request').user
        if user is None:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

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
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        # нужно сделать отображение в списке покупок


#    class FollowShowSerializer(serializers.ModelSerializer):
#    """ Сериализатор модели Подписок (список). """
#    is_subscribed = serializers.SerializerMethodField()
#    recipe = SerializerMethodField()
#    recipes_count = SerializerMethodField()

#    class Meta:
#        model = User
#        fields = (
#            'email',
#            'id',
#            'username',
#            'first_name',
#            'last_name',
#            'is_subscribed',
#            'recipes',
#            'recipes_count'
#        )

#    def get_is_subscribed(self, obj):
#        return (
#            self.context.get('request').user.is_authenticated
#            and Follow.objects.filter(user=self.context['request'].user,
#                                      author=obj).exists())

#    def get_recipes(self, obj):
#        recipes = obj.recipes.all()
#        request = self.context.get('request')
#        limit = request.query_params.get('recipe_limit')
#        if limit:
#            recipes = obj.recipes.all()[:(int(limit))]
#        serializer = RecipeSubscribeSerializer(recipes, many=True)
#        print(serializer.data)
#        return serializer.data

#    def get_recipes_count(self, obj):
#        return obj.recipes.count()


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
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        """ Наличие рецепта в списке покупок. """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user.id).exists()


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
    #    is_subscribed = serializers.SerializerMethodField()
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
#        read_only_fields = ('email', 'id', 'username', 'first_name',
#                            'last_name', 'is_subscribed', 'recipes',
#                            'recipes_count')
#        validators = (validators.UniqueTogetherValidator(
#                    queryset=Follow.objects.all(),
#                    fields=('user', 'author',),
#                    message='Нельзя подписываться дважды на одного автора!'
#                    ),)

#    def get_is_subscribed(self, obj):
#        user = self.context['request'].user
#        return obj.author.get(user=user).exists()

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
        limit = request.GET.get('recipe_limit')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSubscribeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
#        validators = (validators.UniqueTogetherValidator(
#                      queryset=Follow.objects.all(),
#                      fields=('user', 'following',),
#                      message='Нельзя подписываться дважды на одного автора!'
#                      ),)

#    def to_representation(self, instance):
#        return FollowShowSerializer(instance.author, context={
#                                    'request': self.context.get('request')
#                                    }).data
