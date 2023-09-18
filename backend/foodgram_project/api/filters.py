from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter()
    is_favorited = filters.BooleanFilter(method='get'
                                         '_favorite')

    class Meta:
        model = Recipe
        fields = "__all__"

    def get_favorite(self, queryset, value, name):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset
