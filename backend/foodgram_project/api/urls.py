from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from rest_framework.authtoken import views
from .views import (
    IngredientViewSet,
    TagViewSet,
    RecipeViewSet,
    UserViewSet,
    ShoppingCartViewSet,
    FavoriteViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register( r'^recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet, basename='shopping_cart')
router.register( r'^recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorite')
#router.register(
 #   r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
#)
#router.register(
 #   r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
  #  CommentViewSet,
   # basename='comment',
#)


urlpatterns = [
#    path('api-token-auth/', views.obtain_auth_token),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]