from django.shortcuts import get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Follow, Ingredient, Recipe, ShoppingCart,
                            Tag, User)
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .pagination import RecipesPagination
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserSerializer)

# from .filters import IngredientFilter


class GetPostDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.RetrieveModelMixin, viewsets.GenericViewSet,
                           mixins.DestroyModelMixin):
    pass


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = RecipesPagination

#   @action(detail=False, methods=['get'])
#   def subscriptions(self, request):
#        queryset = User.objects.filter(following=request.user)
#        page = self.paginate_queryset(queryset)
#        serializer = FollowSerializer(page, many=True,
#                                      context={'request': request})
#        return self.get_paginated_response(serializer.data)


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


class FollowViewSet(GetPostDeleteViewSet):
    serializer_class = FollowSerializer
    model=Follow

#    def get_queryset(self):
#        authors = self.request.user.follower.values('author').all()
#        return User.objects.filter(id__in=authors).prefetch_related('recipes')

#    def profile_follow(request, username):
#        user = request.user
#        author = get_object_or_404(User, username=username)
#        follow = Follow.objects.create(user=user, author=author)
#        serializer = FollowSerializer(follow)
#        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        return get_list_or_404(User, following=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        author_id = self.kwargs.get('author_id')
        context['recipes_limit'] = self.request.query_params.get(
            'recipes_limit')
        if author_id:
            context['author'] = get_object_or_404(User, id=author_id)
        context['user'] = self.request.user
        return context

    def perform_create(self, serializer):
        user = self.get_serializer_context().get('user')
        author = self.get_serializer_context().get('author')
        serializer.save(user=user, author=author)

    def destroy(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        instance = get_object_or_404(Follow, user=self.request.user,
                                     author=author)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
