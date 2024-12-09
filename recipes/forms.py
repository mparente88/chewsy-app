from django import forms
from .models import Recipe, InstructionStep, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'cook_time']

class InstructionStepForm(forms.ModelForm):
    class Meta:
        model = InstructionStep
        fields = ['step_number', 'content']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']
