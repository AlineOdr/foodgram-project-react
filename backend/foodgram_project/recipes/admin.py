from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe, User)


class UserAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'units_of_measurement',
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'colour',
        'slug'
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount_of_ingredient'
    )
    list_filter = ('recipe', 'ingredient')


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
    )
    list_filter = ('name', 'author', 'tags')
    inlines = (IngredientRecipeInline, TagRecipeInline)
    #   inlines = (TagRecipeInline,)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tag',
        'recipe',
    )
    list_filter = ('recipe', 'tag',)
    empty_value_display = '-пусто-'

class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'following',
        'follower',
    )
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
