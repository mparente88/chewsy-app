from django.urls import path
from .views import (
    RecipeListView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    InstructionStepCreateView,
    InstructionStepDeleteView,
    IngredientCreateView,
    IngredientDeleteView,
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('<int:recipe_id>/steps/create/', InstructionStepCreateView.as_view(), name='step_create'),
    path('steps/<int:pk>/delete/', InstructionStepDeleteView.as_view(), name='step_delete'),
    path('<int:recipe_id>/ingredients/create/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),
]
