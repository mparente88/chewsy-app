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

from django import forms
from decimal import Decimal, InvalidOperation
from fractions import Fraction

class FractionOrDecimalField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        try:
            value = value.strip()
            if '/' in value:
                parts = value.split()
                total_fraction = Fraction(0)
                for part in parts:
                    total_fraction += Fraction(part)

                decimal_value = Decimal(str(float(total_fraction)))
                return decimal_value.quantize(Decimal('0.01'))
            else:
                decimal_value = Decimal(value)
                return decimal_value.quantize(Decimal('0.01'))
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