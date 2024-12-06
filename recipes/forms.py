from django import forms
from .models import Recipe, Category, Tag

class RecipeSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="No Category"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'category', 'tags']

        def clean_title(self):
            title = self.cleaned_data.get('title')
            if len(title) > 200:
                raise forms.ValidationError("Title must be under 200 characters.")
            return title
        
        def clean_ingredients(self):
            ingredients = self.cleaned_data.get('ingredients')
            if not ingredients.strip():
                raise forms.ValidationError("Ingredients cannot be empty.")
            return ingredients

        def clean_instructions(self):
            instructions = self.cleaned_data.get('instructions')
            if not instructions.strip():
                raise forms.ValidationError("Instructions cannot be empty.")
            return instructions
        