from django.contrib import admin
from .models import Recipe, Category, Tag, Direction

class DirectionInline(admin.TabularInline):
    model = Direction
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'category')
    inlines = [DirectionInline]
admin.site.register(Category)
admin.site.register(Tag)


# Register your models here.
