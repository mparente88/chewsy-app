from django.urls import path, register_converter
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView,
    IngredientCreateView, IngredientUpdateView, IngredientDeleteView,
    TagListView, SignUpView, InstructionCreateView, InstructionDeleteView, 
    InstructionUpdateView, AllRecipesListView, MyRecipesListView,
    InstructionReorderView, DuplicateRecipeView, add_to_cookbook, MyCookbookListView,
    shuffle_recipes, HomeView, MealPlanView, AddMealView, EditMealView, DeleteMealView,
    TagManagementView, EditTagView, DeleteTagView, ShoppingListView
)

# ChatGPT helped me with this converter part
# when I asked how to view meal plans
# in the past with the system that I had

class SignedIntConverter:
    regex = r'-?\d+'

    def to_python(self, value):
        return int(value)
    
    def to_url(self, value):
        return str(value)
    
register_converter(SignedIntConverter, 'signed_int')

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': 'home'}, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', HomeView.as_view(), name='home'),
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
    path('meal-plan/<signed_int:week_offset>/', MealPlanView.as_view(), name='meal_plan'),
    path('meal-plan/', MealPlanView.as_view(), {'week_offset': 0}, name='meal_plan'),
    path('meal-plan/<int:meal_plan_id>/add-meal/<slug:day>/<slug:meal_type>/', AddMealView.as_view(), name='add_meal'),
    path('meal-plan/edit-meal/<int:meal_id>/', EditMealView.as_view(), name='edit_meal'),
    path('meal-plan/delete-meal/<int:pk>/', DeleteMealView.as_view(), name='delete_meal'),
    path("superuser/tags/", TagManagementView.as_view(), name="tag_management"),
    path("superuser/tags/edit/<int:tag_id>/", EditTagView.as_view(), name="edit_tag"),
    path("superuser/tags/delete/<int:tag_id>/", DeleteTagView.as_view(), name="delete_tag"),
    path('shopping-list/<slug:start_date>/<slug:end_date>/', ShoppingListView.as_view(), name='shopping_list'),
]
