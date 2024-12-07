from django import forms
from django.forms.models import inlineformset_factory
from .models import Recipe, Category, Tag, Direction, Ingredient

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
        fields = ['title', 'description', 'category', 'tags']

class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ['step_number', 'description']
        widgets = {
            'step_number': forms.HiddenInput(),
        }

DirectionFormSet = inlineformset_factory(
    Recipe,
    Direction,
    form=DirectionForm,
    fields=['step_number', 'description'],
    extra=1,
    can_delete=True
)

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'measurement', 'chef_notes']

IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    fields=['name', 'quantity', 'measurement', 'chef_notes'],
    extra=1,
    can_delete=True
)
