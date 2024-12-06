from django import forms
from django.forms.models import inlineformset_factory
from .models import Recipe, Category, Tag, Direction

class RecipeSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )

    dietary_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='dietary'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    season_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='season'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    time_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='time'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    cuisine_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='cuisine'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    flavor_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='flavor'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    misc_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='misc'),
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
        fields = ['title', 'description', 'ingredients', 'category', 'tags']

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
        
class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ['step_number', 'description']
        widgets = {
            'step': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter step'}),
        }

DirectionFormSet = inlineformset_factory(
    parent_model=Recipe,
    model=Direction,
    form=DirectionForm,
    extra=1,
    can_delete=True
)