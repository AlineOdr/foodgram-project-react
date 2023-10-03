from django import forms
from django.contrib import admin

from .models import (
    Favorite,
    Follow,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    TagRecipe,
    User,
)

# from django.forms.models import BaseInlineFormSet


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
    )
    list_filter = (
        'username',
        'email',
    )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient')


#    class AtLeastNoDoubleIngredientOrTagInlineFormSet(BaseInlineFormSet):
#
#    def clean(self):
#        """Убеждаемся, что тэги и ингредиенты не дублируются."""
#        cleaned_data = super().clean()
#        true_tag = cleaned_data.get("tag")
#        if true_tag:
#            tags = Tag.objects.filter(tag_id=cleaned_data.get("tag_id"))
#            for tag in tags:
#                if tag.true_tag:
#                    raise forms.ValidationError('Нельзя дважды '
#                                                'выбрать один тэг!')
#        return cleaned_data
class IngredientRecipeInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):
        super().clean()
        ingredients = set()
        delete_counter = 0
        for form in self.forms:
            ingredient = form.cleaned_data.get('ingredient')
            amount = form.cleaned_data.get('amount')
            delete = form.cleaned_data.get('DELETE')

            if delete:
                delete_counter += 1
                continue

            if ingredient and amount:
                if ingredient not in ingredients:
                    ingredients.add(ingredient)
                    continue
                raise 'Этот ингредиент уже добавлен!'
        if delete_counter == len(self.forms):
            raise 'Нельзы сохранить рецепт без ингредиента!'

        if not ingredients:
            raise 'Нельзы сохранить рецепт без ингредиента!'


class TagRecipeInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        tags = set()
        delete_counter = 0
        for form in self.forms:
            tag = form.cleaned_data.get('tag')
            delete = form.cleaned_data.get('DELETE')

            if delete:
                delete_counter += 1
                continue

            if tag:
                if tag not in tags:
                    tags.add(tag)
                    continue
                raise 'Этот тэг уже добавлен!'
        if delete_counter == len(self.forms):
            raise 'Нельзы сохранить рецепт без тэга!'

        if not tags:
            raise 'Нельзы сохранить рецепт без тэга!'
        tags = set()

#   class AtLeastOneIngredientOrTagInlineFormSet(BaseInlineFormSet):
#
#    def clean(self):
#        """Убеждаемся, что введен хотя бы один тэг и ингредиент."""
#        super(AtLeastOneIngredientOrTagInlineFormSet, self).clean()
#        if any(self.errors):
#            return
#        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
#                   for cleaned_data in self.cleaned_data):
#            raise forms.ValidationError('Нельзя сохранить рецепт '
#                                        'без тэгов и ингредиентов.')


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1
    min_num = 1
    formset = TagRecipeInlineFormset


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    min_num = 1
    formset = IngredientRecipeInlineFormset


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'get_favorited_count',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    inlines = (IngredientRecipeInline, TagRecipeInline)
    empty_value_display = '-пусто-'

    def get_favorited_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    get_favorited_count.short_description = 'В избранном у пользователей'


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
    list_filter = (
        'recipe',
        'tag',
    )
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
