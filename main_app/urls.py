from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView,
    IngredientCreateView, IngredientUpdateView, IngredientDeleteView,
    TagListView
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/<int:recipe_id>/ingredient/new/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredient/<int:pk>/edit/', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('tags/', TagListView.as_view(), name='tag_list'),
]
