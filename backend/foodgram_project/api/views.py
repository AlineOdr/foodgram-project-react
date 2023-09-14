from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Follow, Ingredient, Recipe, ShoppingCart,
                            Tag, User)
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from .pagination import RecipesPagination
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserSerializer)

# from .filters import IngredientFilter


class GetPostViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = RecipesPagination

    def profile_follow(self, request, username):
        #    user = request.user
        following = get_object_or_404(User, username=username)
        if following != request.user:
            Follow.objects.get_or_create(user=request.user, following=following)
        return Response(status=status.HTTP_201_CREATED)

#    def subscriptions(self, request):
#       user = request.user
#      queryset = User.objects.filter(following=user)
#     page = self.paginate_queryset(queryset)
#    serializer = SubscribedShowSerializer(
#           page, many=True,
#          context={'request': request})
# return self.get_paginated_response(serializer.data)


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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = RecipesPagination
#    filterset_class = IngredientFilter

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

    #   def perform_create(self, serializer):
    #      serializer.save(author=self.request.user.id)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

#    def downloadshopping_cart(self, request):
#        user = request.user


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FollowViewSet(GetPostViewSet):
    """ Отображение подписок. """
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()
#    def subscriptions(self, request):
#       user = request.user
#      queryset = User.objects.filter(following=user)
#     page = self.paginate_queryset(queryset)
#    serializer = SubscribedShowSerializer(
#       page, many=True,
#      context={'request': request})
#        return self.get_paginated_response(serializer.data)
