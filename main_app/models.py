from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    servings = models.IntegerField()
    image = models.ImageField(upload_to='main_app/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_time(self):
        return self.prep_time + self.cook_time

class Ingredient(models.Model):
    MEASUREMENT_CHOICES = [
        ("pinch", "Pinch"),
        ("teaspoon", "Teaspoon"),
        ("tablespoon", "Tablespoon"),
        ("cup", "Cup"),
        ("ounce", "Ounce"),
        ("pound", "Pound"),
        ("gram", "Gram"),
        ("kilogram", "Kilogram"),
        ("milliliter", "Milliliter"),
        ("liter", "Liter"),
        ("piece", "Piece"),
        ("dash", "Dash"),
        ("handful", "Handful"),
        ("slice", "Slice"),
        ("clove", "Clove"),
    ]
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    measurement = models.CharField(max_length=20, choices=MEASUREMENT_CHOICES)
    order = models.IntegerField(null=True, blank=True)

class Tag(models.Model):
    TAG_CATEGORY_CHOICES = [
        ("season", "Season"),
        ("taste", "Taste"),
        ("time", "Time"),
        ("complexity", "Complexity"),
        ("cuisine", "Cuisine"),
        ("diet", "Diet"),
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=TAG_CATEGORY_CHOICES)
    recipes = models.ManyToManyField(Recipe, related_name="tags", blank=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
