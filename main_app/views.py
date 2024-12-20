from django import forms
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseRedirect
from django.db import models
from django.db.models import Count
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe, Ingredient, Tag, Instruction, UserCookbook, MealPlan, Meal
from .forms import RecipeForm, IngredientForm, InstructionForm, MealForm
from datetime import date, timedelta
from decimal import Decimal
from fractions import Fraction
import random

# Recipes

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
    paginate_by = 12

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

class AllRecipesListView(ListView):
    model = Recipe
    template_name = 'all_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 12

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

        context['tags'] = Tag.objects.all()
        context['selected_tags'] = [
            int(tag) for tag in self.request.GET.getlist('tags') if tag.isdigit()
        ]
        context['tag_categories'] = {
            category: Tag.objects.filter(category=category)
            for category, _ in Tag.TAG_CATEGORY_CHOICES
        }

        if user.is_authenticated:
            cookbook, created = UserCookbook.objects.get_or_create(user=user)
            cookbook_recipes = cookbook.recipes.all()
            context['my_cookbook'] = cookbook_recipes
            if cookbook_recipes.exists():
                context['random_recipe'] = random.choice(list(cookbook_recipes))

        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.path)
    
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'
    
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

class TagManagementView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def get(self, request):
        categories = Tag.TAG_CATEGORY_CHOICES
        tags = Tag.objects.all()
        return render(request, 'superuser/tag_management.html', {
            'categories': categories,
            'tags': tags,
        })
    
    def post(self, request):
        tag_name = request.POST.get('tag_name')
        tag_category = request.POST.get('tag_category')

        if tag_name and tag_category:
            valid_categories = [choice[0] for choice in Tag.TAG_CATEGORY_CHOICES]
            if tag_category not in valid_categories:
                messages.error(request, "Invalid category selected.")
            else:
                Tag.objects.create(name=tag_name, category=tag_category)
                messages.success(request, f"Tag '{tag_name}' added to category '{tag_category}'.")
        else:
            messages.error(request, "Both tag name and category are required.")

        return redirect('tag_management')
    
@method_decorator(csrf_exempt, name='dispatch')
class EditTagView(View):
    def post(self, request, tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
            tag_name = request.POST.get("name")
            tag_category = request.POST.get("category")

            if tag_name:
                tag.name = tag_name
            if tag_category in dict(Tag.TAG_CATEGORY_CHOICES):
                tag.category = tag_category

            tag.save()
            return JsonResponse({"success": True, "message": "Tag updated successfully."})
        except Tag.DoesNotExist:
            return JsonResponse({"success": False, "message": "Tag not found."}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteTagView(View):
    def post(self, request, tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
            tag.delete()
            return JsonResponse({"success": True, "message": "Tag deleted successfully."})
        except Tag.DoesNotExist:
            return JsonResponse({"success": False, "message": "Tag not found."}, status=404)

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

# Meals and Meal Plans

class MealPlanView(LoginRequiredMixin, View):
    def get(self, request, week_offset=0):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)

        meal_plan, created = MealPlan.objects.get_or_create(user=request.user, start_date=start_of_week)

        days = [start_of_week + timedelta(days=i) for i in range(7)]
        meal_types = ['breakfast', 'lunch', 'dinner', 'snack']

        meals = meal_plan.meals.all()
        meals_by_day = {d: {mt: None for mt in meal_types} for d in days}
        for meal in meals:
            meals_by_day[meal.date][meal.meal_type] = meal

        table_rows = []
        for mt in meal_types:
            row = []
            for d in days:
                row.append((d, meals_by_day[d][mt]))
            table_rows.append((mt, row))

        context = {
            'meal_plan': meal_plan,
            'days': days,
            'meal_types': meal_types,
            'table_rows': table_rows,
            'week_offset': week_offset,
            'week_start': start_of_week,
            'week_end': end_of_week,
        }

        return render(request, 'meal_plan.html', context)

    
class AddMealView(LoginRequiredMixin, View):
    def get(self, request, meal_plan_id, day, meal_type):
        form = MealForm()
        return render(request, 'add_meal.html', {'form': form, 'day': day, 'meal_type': meal_type})
    
    def post(self, request, meal_plan_id, day, meal_type):
        meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id, user=request.user)
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.meal_plan = meal_plan
            meal.date = day
            meal.meal_type = meal_type
            meal.save()
            return redirect('meal_plan')
        return render(request, 'add_meal.html', {'form': form, 'day': day, 'meal_type': meal_type})

class EditMealView(LoginRequiredMixin, View):
    def get(self, request, meal_id):
        meal = get_object_or_404(Meal, pk=meal_id, meal_plan__user=request.user)
        form = MealForm(instance=meal)
        return render(request, 'edit_meal.html', {'form': form, 'meal': meal})
    
    def post(self, request, meal_id):
        meal = get_object_or_404(Meal, pk=meal_id, meal_plan__user=request.user)
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('meal_plan')
        return render(request, 'edit_meal.html', {'form': form, 'meal': meal})

class DeleteMealView(LoginRequiredMixin, DeleteView):
    model = Meal
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('meal_plan')

# Authentication/Authorization

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

# Shopping List

class ShoppingListView(LoginRequiredMixin, View):
    def get(self, request, start_date, end_date):
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

        meals = Meal.objects.filter(
            meal_plan__user=request.user,
            date__range=(start_date, end_date)
        ).select_related('recipe')

        ingredient_data = {}

        for meal in meals:
            if meal.recipe:
                for ingredient in meal.recipe.ingredients.all():
                    key = (ingredient.name, ingredient.measurement)
                    note = ingredient.notes or ""

                    if key not in ingredient_data:
                        ingredient_data[key] = {'total_quantity': Decimal(0), 'notes': []}

                    ingredient_data[key]['total_quantity'] += ingredient.quantity
                    if note:
                        ingredient_data[key]['notes'].append(f"{ingredient.quantity} {note}")

        combined_ingredients = [
            {
                'name': name,
                'measurement': measurement,
                'total_quantity': data['total_quantity'],
                'notes': "; ".join(set(data['notes']))
            }
            for (name, measurement), data in ingredient_data.items()
        ]

        combined_ingredients.sort(key=lambda x: x['name'].lower())

        context = {
            'ingredients': combined_ingredients,
            'start_date': start_date,
            'end_date': end_date
        }
        return render(request, 'shopping_list.html', context)


