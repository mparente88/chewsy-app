from django.contrib import admin
from .models import Recipe, Ingredient, Tag

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'prep_time', 'cook_time', 'total_time', 'servings', 'created_at')
    list_filter = ('user', 'created_at', 'tags')
    search_fields = ('title', 'description')
    autocomplete_fields = ('tags',)
    prepopulated_fields = {'total_time': ('prep_time', 'cook_time')}

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'measurement', 'recipe')
    list_filter = ('measurement',)
    search_fields = ('name',)
    ordering = ('recipe', 'order')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
