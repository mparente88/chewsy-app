from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import Recipe, Ingredient, Tag, Instruction
from .forms import RecipeForm, IngredientForm, InstructionForm

# Recipes

class MyRecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'my_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.filter(user=self.request.user)
        tag_ids = self.request.GET.getlist('tags')
        if tag_ids:
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tags'] = [int(tag) for tag in self.request.GET.getlist('tags') if tag.isdigit()]
        context['tag_categories'] = {
            category: Tag.objects.filter(category=category)
            for category, _ in Tag.TAG_CATEGORY_CHOICES
        }
        return context
    
class AllRecipesListView(ListView):
    model = Recipe
    template_name = 'all_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.all()
        tag_ids = self.request.GET.getlist('tags') 
        if tag_ids:
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all() 
        context['selected_tags'] = [int(tag) for tag in self.request.GET.getlist('tags') if tag.isdigit()] 
        context['tag_categories'] = {
            category: Tag.objects.filter(category=category)
            for category, _ in Tag.TAG_CATEGORY_CHOICES
        }
        return context


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)
    
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)
    
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})
    
class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        recipe = self.get_object()
        return recipe.user == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})
    
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

    def test_func(self):
        recipe = self.get_object()
        return recipe.user == self.request.user
    
# Ingredients

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredient_form.html'

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        return context

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.kwargs['recipe_id']})
    
class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredient_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        return context

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.object.recipe.pk})
    
class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'ingredient_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})
    
# Tags

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'

# Instructions

class InstructionCreateView(CreateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'instruction_form.html'

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        form.instance.recipe = recipe
        if not form.instance.step_number:
            form.instance.step_number = recipe.instructions.count() + 1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = get_object_or_404(Recipe, pk=self.kwargs['recipe_id'])
        return context

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.kwargs['recipe_id']})

from django.shortcuts import get_object_or_404
from django.urls import reverse

class InstructionUpdateView(UpdateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'instruction_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        return context

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.object.recipe.pk})

class InstructionDeleteView(DeleteView):
    model = Instruction
    template_name = 'instruction_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        instruction = self.get_object()
        recipe = instruction.recipe
        instruction.delete()

        for index, step in enumerate(recipe.instructions.all(), start=1):
            step.step_number = index
            step.save()

        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.object.recipe.pk})



# Authentication/Authorization

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')