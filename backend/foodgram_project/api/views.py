from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Follow, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag, User)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .filters import RecipeFilter
from .pagination import RecipesPagination
from .permissions import AuthorAdminOrAuthenticatedReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserSerializer)


class CustomUserViewSet(UserViewSet):
    """ Класс для кастомной модели юзера."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = RecipesPagination

    @action(
        detail=True, permission_classes=[IsAuthenticated],
        methods=["POST", "DELETE"],
    )
    def subscribe(self, request, id):
        """ Подписка на пользоватедя."""
        user = request.user
        author = get_object_or_404(User, id=id)

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
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('name',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorAdminOrAuthenticatedReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = RecipesPagination
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeSerializer

    @action(detail=True, methods=["POST", "DELETE"],)
    def favorite(self, request, pk):
        user = request.user
        if request.method == "POST":
            if not Favorite.objects.filter(user=user, recipe=pk).exists():
                recipe = get_object_or_404(Recipe, pk=pk)
                serializer = FavoriteSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        if Favorite.objects.filter(user=user, recipe=pk).delete()[0] == 0:
            return Response(
                'Такого рецепта нет в избранном.',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Рецепт удален из избранного', status=status.HTTP_204_NO_CONTENT
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
        if ShoppingCart.objects.filter(user=user, recipe=pk).delete()[0] == 0:
            return Response(
                'Такого рецепта нет в списке покупок.',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response('Рецепт удален!', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        """ скачать список покупок."""
        user = self.request.user
        ingredient = IngredientRecipe.objects.filter(
            recipe__shopping_cart_recipes__user=user).values(
            'ingredients__name',
            'ingredients__units_of_measurement'
        ).annotate(
            amount=Sum('amount')
        )
        text = 'список'
        for ing, ingredient in enumerate(ingredients, start=1):
            text += (
                f'{ing}. {ingredient[0]} - '
                f'{ingredient[1]} '
                f'{ingredient[2]}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; ' 'filename="shopping_list.txt"'
        )
        return response
