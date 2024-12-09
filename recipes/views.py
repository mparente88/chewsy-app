from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Recipe, InstructionStep, Ingredient
from .forms import RecipeForm, InstructionStepForm, IngredientForm

# Recipe Views
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_list')


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_success_url(self):
        return reverse_lazy('recipe_list')


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')


# InstructionStep Views
class InstructionStepCreateView(CreateView):
    model = InstructionStep
    form_class = InstructionStepForm
    template_name = 'recipes/step_form.html'

    def form_valid(self, form):
        recipe = Recipe.objects.get(id=self.kwargs['recipe_id'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_update', kwargs={'pk': self.kwargs['recipe_id']})


class InstructionStepDeleteView(DeleteView):
    model = InstructionStep
    template_name = 'recipes/step_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('recipe_update', kwargs={'pk': self.object.recipe.id})


# Ingredient Views
class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipes/ingredient_form.html'

    def form_valid(self, form):
        recipe = Recipe.objects.get(id=self.kwargs['recipe_id'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_update', kwargs={'pk': self.kwargs['recipe_id']})


class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'recipes/ingredient_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('recipe_update', kwargs={'pk': self.object.recipe.id})
