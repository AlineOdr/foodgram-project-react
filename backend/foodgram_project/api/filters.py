from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag, Ingredient


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='get'
                                         '_favorite')
    is_in_shopping_cart = filters.BooleanFilter(method='get_is_in_'
                                                       'shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('author',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'tags')

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                shopping_cart_recipes__user=self.request.user
            )
        return queryset

    def get_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)
        return queryset


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ('name')
