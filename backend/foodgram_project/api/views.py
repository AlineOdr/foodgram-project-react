from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Follow, Ingredient, Recipe, ShoppingCart,
                            Tag, User)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .filters import RecipeFilter
from .pagination import RecipesPagination
from .permissions import AuthorAdminOrReadOnly, IsAdminOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserSerializer)


class GetPostDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.RetrieveModelMixin, viewsets.GenericViewSet,
                           mixins.DestroyModelMixin):
    pass


class CustomUserViewSet(UserViewSet):
    """ Класс для кастомной модели юзера."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = RecipesPagination

    @action(
        detail=True, permission_classes=[IsAuthenticated],
        methods=["POST", "DELETE"],
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, pk=pk)

        if request.method == 'POST':
            if author == user:
                raise ValidationError(
                    {'errors': 'Вы не можете быть подписаны на самого себя!'}
                )
            if Follow.objects.filter(user=user, author=author).exists():
                raise ValidationError({'errors':
                                       'Нельзя подписываться дважды'
                                       'на одного автора!'})
            serializer = FollowSerializer(
                author, context={'request': request}
            )
            Follow.objects.create(user=user, author=author)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=["GET"])
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        serializer = FollowSerializer(self.paginate_queryset(queryset),
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('name,')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
#    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = RecipesPagination
#    filterset_class = IngredientFilter
    filterset_class = RecipeFilter

#    def get_queryset(self):
#        recipe = Recipe.objects.all()
#        return recipe
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        # Если запрошенное действие (action)
        #  — получение списка объектов ('list')
        if self.request.method == 'GET':
            # ...то применяем CatListSerializer
            return RecipeSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return RecipeSerializer

    @action(detail=True, methods=["POST", "DELETE"],)
    def favorite(self, request, pk):
        user = request.user
        if not Favorite.objects.filter(user=user, recipe=pk).exists():
            recipe = get_object_or_404(Recipe, pk=pk)
            serializer = FavoriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            "Рецепт удален из избранного", status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=["POST", "DELETE"],)
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == "POST":
            if not ShoppingCart.objects.filter(user=user, recipe=pk).exists():
                recipe = get_object_or_404(Recipe, pk=pk)
                serializer = ShoppingCartSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        return Response('Рецепт удален!', status=status.HTTP_204_NO_CONTENT)


#    class DownloadShoppingCart(sviewsets.ModelViewSet):
#    пока не понимаю как реализовать
#    def get_shopping_cart(self, request):
#        """ скачать список покупок."""
#        user = request.user
#        ingredients = IngredientRecipe.object.filter(
#        shopping_cart_recipes__recipe=user).
#     values("ingredients__name",
#                                    "ingredients__units_of_measurement")
#        buffer = io.BytesIO()
#        response FileResponse(open('shopping_list.txt'))
