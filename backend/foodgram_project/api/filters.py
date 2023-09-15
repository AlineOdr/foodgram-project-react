#    import django_filters

#    from recipes.models import Recipe


#    class RecipeFilter(django_filters.FilterSet):
#    tags = django_filters.CharFilter(field_name='filter_tag')
#    is_favorited = django_filters.CharFilter(method='get_is_favorited')
#    is_in_shopping_cart = django_filters.CharFilter(method=
#       'get_is_in_shopping_cart ')

#    class Meta:
#        model = Title
#        fields = "__all__"
