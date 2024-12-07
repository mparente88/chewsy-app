from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from .models import Recipe, Category, Tag, Direction
from .forms import RecipeForm, RecipeSearchForm, DirectionFormSet, IngredientFormSet

class HomeView(TemplateView):
    template_name = 'recipes/home.html'

class SignupView(FormView):
    template_name = 'recipes/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your account has been created. Please log in.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Signup failed. Correct errors.")
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class LoginView(FormView):
    template_name = 'recipes/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        next_url = self.request.POST.get('next') or 'home'
        return redirect(next_url)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12 
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RecipeSearchForm(self.request.GET or None)
        context['form'] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = RecipeSearchForm(self.request.GET or None)

        if form.is_valid():
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            
            dietary_tags = form.cleaned_data.get('dietary_tags')
            if dietary_tags:
                for t in dietary_tags:
                    queryset = queryset.filter(tags=t)
            
            season_tags = form.cleaned_data.get('season_tags')
            if season_tags:
                for t in season_tags:
                    queryset = queryset.filter(tags=t)

            time_tags = form.cleaned_data.get('time_tags')
            if time_tags:
                for t in time_tags:
                    queryset = queryset.filter(tags=t)

            cuisine_tags = form.cleaned_data.get('cuisine_tags')
            if cuisine_tags:
                for t in cuisine_tags:
                    queryset = queryset.filter(tags=t)

            flavor_tags = form.cleaned_data.get('flavor_tags')
            if flavor_tags:
                for t in flavor_tags:
                    queryset = queryset.filter(tags=t)

            misc_tags = form.cleaned_data.get('misc_tags')
            if misc_tags:
                for t in misc_tags:
                    queryset = queryset.filter(tags=t)

        return queryset

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

from django.db import transaction

from django.db import transaction

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipe_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['direction_formset'] = DirectionFormSet(self.request.POST)
            context['ingredient_formset'] = IngredientFormSet(self.request.POST)
        else:
            context['direction_formset'] = DirectionFormSet()
            context['ingredient_formset'] = IngredientFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        direction_formset = context['direction_formset']
        ingredient_formset = context['ingredient_formset']
        form.instance.user = self.request.user

        if direction_formset.is_valid() and ingredient_formset.is_valid():
            self.object = form.save()

            directions = direction_formset.save(commit=False)
            for direction in directions:
                direction.recipe = self.object
                direction.save()

            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = self.object
                ingredient.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(self.request.POST, instance=self.object)
        else:
            context['ingredient_formset'] = IngredientFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        with transaction.atomic():
            self.object = form.save()
            if ingredient_formset.is_valid():
                ingredients = ingredient_formset.save(commit=False)
                for ingredient in ingredients:
                    ingredient.recipe = self.object
                    ingredient.save()
                ingredient_formset.save_m2m()
                def get_success_url(self):
                    return reverse('recipe_detail', kwargs={'pk': self.object.pk})
            else:
                return self.form_invalid(form)
        return super().form_valid(form)




class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You are not allowed to delete this recipe.")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Recipe successfully deleted!")
        return super().delete(request, *args, **kwargs)
