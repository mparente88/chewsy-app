from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView,
    IngredientCreateView, IngredientUpdateView, IngredientDeleteView,
    TagListView, SignUpView, InstructionCreateView, InstructionDeleteView, 
    InstructionUpdateView, AllRecipesListView, MyRecipesListView,
    InstructionReorderView, DuplicateRecipeView, add_to_cookbook, MyCookbookListView,
    shuffle_recipes
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', AllRecipesListView.as_view(), name='recipe_list'),
    path('my-recipes/', MyRecipesListView.as_view(), name='my_recipes'),
    path('all-recipes/', AllRecipesListView.as_view(), name='all_recipes'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/<int:recipe_id>/ingredient/new/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredient/<int:pk>/edit/', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('recipe/<int:recipe_id>/instruction/new/', InstructionCreateView.as_view(), name='instruction_create'),
    path('instruction/<int:pk>/edit/', InstructionUpdateView.as_view(), name='instruction_update'),
    path('instruction/<int:pk>/delete/', InstructionDeleteView.as_view(), name='instruction_delete'),
    path('recipe/<int:recipe_id>/instructions/reorder/', InstructionReorderView.as_view(), name='instructions_reorder'),
    path('recipe/<int:pk>/duplicate/', DuplicateRecipeView.as_view(), name='recipe_duplicate'),
    path('recipe/<int:pk>/cookbook/', add_to_cookbook, name='add_to_cookbook'),
    path('my-cookbook/', MyCookbookListView.as_view(), name='my_cookbook'),
    path('shuffle-recipes/', views.shuffle_recipes, name='shuffle_recipes'),
]
