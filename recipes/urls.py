from django.urls import path
from recipes.views import (
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
)

app_name = 'recipes'

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),  # /recipes/
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),  # /recipes/15/
    path('new/', RecipeCreateView.as_view(), name='recipe_create'),  # /recipes/new/
    path('<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),  # /recipes/15/edit/
    path('<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),  # /recipes/15/delete/
]