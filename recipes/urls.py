from django.urls import path
from django.shortcuts import render
from . import views

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/create/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:pk>/edit/', views.recipe_update, name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
]
