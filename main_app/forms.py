from django import forms
from .models import Recipe, Ingredient, Instruction, Tag

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'cook_time', 'servings', 'image', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'measurement']

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['description', 'time_minutes']