from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter()
    is_favorited = filters.BooleanFilter(method='get'
                                         '_favorite')
    is_in_shopping_cart = filters.BooleanFilter(method='get_is_in_'
                                                       'shopping_cart')
    tags = filters.CharFilter()

    class Meta:
        model = Recipe
        fields = ('author',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'tags')

    def get_is_in_shopping_cart(self, queryset, value):
        if value:
            return queryset.filter(
                shopping_cart_recipes__user=self.request.user
            )
        return queryset

    def get_favorite(self, queryset, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)
        return queryset
