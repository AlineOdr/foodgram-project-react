from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from rest_framework.authtoken import views
from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingCartViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'^recipes/(?P<recipe_id>\d+)/shopping_cart',
                ShoppingCartViewSet, basename='shopping_cart')
router.register(r'^recipes/download_shopping_cart',
                ShoppingCartViewSet, basename='shopping_cart')
#    router.register(r'^recipes/(?P<recipe_id>\d+)/favorite',
#                FavoriteViewSet, basename='favorite')
#    router.register(r'^users/subscriptions',
#                FollowViewSet,  basename='subscriptions')
#    router.register(r'^users/(?P<author_id>\d+)/subscribe',
#                FollowViewSet, basename='subscribe')

urlpatterns = [
     #    path('users/subscriptions/', FollowViewSet.as_view({'get': 'list'}),
     #          name='subscriptions'),
     #    path('users/<int:author_id>/subscribe/',
     #     FollowViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
     #     name='subscribe'),
     path('auth/', include('djoser.urls.authtoken')),
     path('', include(router.urls)),
     path('', include('djoser.urls'))
]
