from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter()
    is_favorited = filters.BooleanFilter(method='get'
                                         '_favorite')

    class Meta:
        model = Recipe
        fields = ("author",
                  "is_favorited")

    def get_favorite(self, queryset, value, name):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)
        return queryset
