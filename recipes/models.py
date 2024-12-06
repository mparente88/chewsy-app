from django.db import models
from django.conf import settings

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class Direction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="directions")
    step_number = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.recipe.title} - Step {self.step_number}"


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
