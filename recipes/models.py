from django.db import models
from django.contrib.auth.models import User

# Recipe model
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    def __str__(self):
        return self.title

# InstructionStep model
class InstructionStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    content = models.TextField() 

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.title}"

# Ingredient model
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name} for {self.recipe.title}"

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    recipes = models.ManyToManyField(Recipe, related_name='categories')

    def __str__(self):
        return self.name
