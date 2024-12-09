from django.shortscuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Recipe, InstructionStep, Ingredient

class RecipeListCreateView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        recipe_list = [{"id": recipe.id, "title": recipe.title, "description": recipe.description} for recipe in recipes]
        return JsonResponse(recipe_list, safe=False)
    
    def post(self, request):
        data = request.POST
        recipe = Recipe.objects.create(
            title=data.get("title"),
            description=data.get("description"),
            prep_time=data.get("prep_time"),
            cook_time=data.get("cook_time"),
            user=request.user
        )
        return JsonResponse({"id": recipe.id, "message": "Recipe created successfully!"})

