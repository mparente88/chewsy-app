from django.http import HttpResponseRedirect, JsonResponse
from django.db import models
from django.db.models import Count
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe, Ingredient, Tag, Instruction, UserCookbook
from .forms import RecipeForm, IngredientForm, InstructionForm
import random

# Recipes

from django.views.generic import ListView
from django.db import models
from .models import Recipe, Tag
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cookbook, created = UserCookbook.objects.get_or_create(user=user)
            context['my_cookbook'] = cookbook.recipes.all()
            if cookbook.recipes.exists():
                context['random_recipe'] = random.choice(list(cookbook.recipes.all()))
        return context

class MyRecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'my_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.filter(user=self.request.user)

        tag_ids = self.request.GET.getlist('tags')
        if tag_ids:
            queryset = (
                queryset.filter(tags__id__in=tag_ids) 
                .annotate(tag_count=models.Count('tags')) 
                .filter(tag_count=len(tag_ids))  
            )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all() 
        context['selected_tags'] = [int(tag) for tag in self.request.GET.getlist('tags') if tag.isdigit()]
        context['tag_categories'] = {
            category: Tag.objects.filter(category=category)
            for category, _ in Tag.TAG_CATEGORY_CHOICES
        }
        return context

from django.http import HttpResponseRedirect

class AllRecipesListView(ListView):
    model = Recipe
    template_name = 'all_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipe.objects.all().order_by('-created_at')

        tag_ids = self.request.GET.getlist('tags')
        if tag_ids:
            queryset = (
                queryset.filter(tags__id__in=tag_ids)
                .annotate(tag_count=models.Count('tags'))
                .filter(tag_count=len(tag_ids))
            )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            cookbook, created = UserCookbook.objects.get_or_create(user=user)
            cookbook_recipes = cookbook.recipes.all()
            context['my_cookbook'] = cookbook_recipes
            if cookbook_recipes.exists():
                context['random_recipe'] = random.choice(list(cookbook_recipes))

        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.path)

    
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
    
class DuplicateRecipeView(View):
    def post(self, request, pk, *args, **kwargs):
        original_recipe = get_object_or_404(Recipe, pk=pk, user=request.user)

        duplicated_recipe = Recipe.objects.create(
            title=f"Copy of {original_recipe.title}",
            description=original_recipe.description,
            user=request.user,
            prep_time=original_recipe.prep_time,
            cook_time=original_recipe.cook_time,
            servings=original_recipe.servings,
            image=original_recipe.image,
        )

        duplicated_recipe.tags.set(original_recipe.tags.all())

        for ingredient in original_recipe.ingredients.all():
            Ingredient.objects.create(
                recipe=duplicated_recipe,
                name=ingredient.name,
                quantity=ingredient.quantity,
                measurement=ingredient.measurement,
                order=ingredient.order,
            )

        for instruction in original_recipe.instructions.all():
            Instruction.objects.create(
                recipe=duplicated_recipe,
                step_number=instruction.step_number,
                description=instruction.description,
                time_minutes=instruction.time_minutes,
            )
        messages.success(request, "Recipe duplicated successfully!")
        return redirect('recipe_detail', pk=duplicated_recipe.pk)
    
@login_required
def shuffle_recipes(request):
    cookbook = request.user.cookbook
    cookbook_recipes = list(cookbook.recipes.all())
    if cookbook_recipes:
        random_recipe = random.choice(cookbook_recipes)
        recipe_data = {
            'id': random_recipe.id,
            'title': random_recipe.title,
            'prep_time': random_recipe.prep_time,
            'cook_time': random_recipe.cook_time,
            'image': random_recipe.image.url if random_recipe.image else '/static/images/placeholder.jpg',
        }
        return JsonResponse({'recipe': recipe_data})
    else:
        return JsonResponse({'recipe': None})

# Ingredients

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredient_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        if form.instance.order is None:
            form.instance.order = self.recipe.ingredients.count() + 1
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.recipe.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.recipe
        return context

class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredient_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient = self.object
        context['recipe'] = ingredient.recipe
        return context

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})


class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'ingredient_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe_id})
    
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

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        if not form.instance.step_number:
            form.instance.step_number = self.recipe.instructions.count() + 1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.recipe
        return context

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.recipe.pk})

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
    
class InstructionReorderView(LoginRequiredMixin, View):
    template_name = 'instruction_reorder.html'

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id, user=request.user)
        instructions = recipe.instructions.order_by('step_number')
        return render(request, self.template_name, {'recipe': recipe, 'instructions': instructions})
    
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id, user=request.user)
        new_order = request.POST.getlist('order[]', [])

        for index, instr_id in enumerate(new_order, start=1):
            instruction = recipe.instructions.get(pk=instr_id)
            instruction.step_number = index
            instruction.save()

        return redirect('recipe_detail', pk=recipe.pk)
    
# Cookbook

@login_required
def add_to_cookbook(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    cookbook, created = UserCookbook.objects.get_or_create(user=request.user)
    if recipe in cookbook.recipes.all():
        cookbook.recipes.remove(recipe)
    else:
        cookbook.recipes.add(recipe)
    return redirect('recipe_detail', pk=pk)

class MyCookbookListView(ListView):
    model = Recipe
    template_name = 'my_cookbook.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        cookbook, created = UserCookbook.objects.get_or_create(user=self.request.user)
        return cookbook.recipes.all()

# Authentication/Authorization

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')