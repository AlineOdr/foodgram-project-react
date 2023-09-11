from rest_framework.pagination import PageNumberPagination


class RecipesPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class SubscriptionsPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'recipes_limit'
