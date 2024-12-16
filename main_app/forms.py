from django import forms
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from fractions import Fraction
from .models import Recipe, Ingredient, Instruction, Tag, Meal

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'cook_time', 'servings', 'image', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class FractionOrDecimalField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        try:
            if '/' in value:
                fraction = sum(Fraction(part) for part in value.split())
                decimal_value = Decimal(float(fraction))
                return decimal_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except (ValueError, ZeroDivisionError, InvalidOperation):
            raise forms.ValidationError(
                "Invalid quantity. Please enter a valid number or fraction (e.g., '1', '1/2', '2.5', '2 1/3')."
            )

class IngredientForm(forms.ModelForm):
    quantity = FractionOrDecimalField()

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'measurement']

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['description', 'time_minutes']

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['recipe', 'servings']