#  from django import forms
from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet

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

# from django.core.exceptions import ValidationError


#    from django.forms.models import BaseInlineFormSet
# from django.forms import BaseModelForm


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


#   class IngredientRecipeInlineForm(forms.ModelForm):
#    def is_valid(self):
#        return super(IngredientRecipeInlineForm, self).is_valid

#    def clean(self):
#        count = 0
#        for form in self.forms:
#            try:
#                if form.cleaned_data and not form.cleaned_data.get(
#                    'DELETE', False
#                ):
#                    count += 1
#            except AttributeError:
#                pass
#        if count < 1:
#            raise ValidationError(
#                'Нельзя сохранить рецепт без тэгов и ингредиентов!'
#            )
class AtLeastOneIngredientOrTagInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """Check that at least one service has been entered."""
        super(AtLeastOneIngredientOrTagInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
                   for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least one item required.')


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1
    min_num = 1
    formset = AtLeastOneIngredientOrTagInlineFormSet


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    min_num = 1
    formset = AtLeastOneIngredientOrTagInlineFormSet
#    formset = IngredientRecipeInlineForm


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
#   form = IngredientRecipeInlineForm

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
