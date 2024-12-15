from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    servings = models.IntegerField()
    image = models.ImageField(upload_to='main_app/', null=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='recipes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_time(self):
        return self.prep_time + self.cook_time
    
    def total_cookbooks(self):
        return self.cookbooks.count()
    
    def __str__(self):
        return self.title

class Ingredient(models.Model):
    MEASUREMENT_CHOICES = [
        ("pinch", "Pinch"),
        ("dash", "Dash"),
        ("drop", "Drop"),
        ("smidgen", "Smidgen"),
        ("teaspoon", "Teaspoon"),
        ("tablespoon", "Tablespoon"),
        ("cup", "Cup"),
        ("fluid_ounce", "Fluid Ounce"),
        ("ounce", "Ounce"),
        ("pound", "Pound"),
        ("milligram", "Milligram"),
        ("gram", "Gram"),
        ("kilogram", "Kilogram"),
        ("milliliter", "Milliliter"),
        ("centiliter", "Centiliter"),
        ("deciliter", "Deciliter"),
        ("liter", "Liter"),
        ("quart", "Quart"),
        ("pint", "Pint"),
        ("gallon", "Gallon"),
        ("piece", "Piece"),
        ("slice", "Slice"),
        ("clove", "Clove"),
        ("stick", "Stick"),
        ("stalk", "Stalk"),
        ("leaf", "Leaf"),
        ("head", "Head"),
        ("handful", "Handful"),
        ("bunch", "Bunch"),
        ("sprig", "Sprig"),
        ("cube", "Cube"),
        ("can", "Can"),
        ("jar", "Jar"),
        ("bottle", "Bottle"),
        ("bag", "Bag"),
        ("pack", "Pack"),
        ("box", "Box"),
        ("bar", "Bar"),
        ("sheet", "Sheet"),
        ("square", "Square"),
        ("ring", "Ring"),
        ("roll", "Roll"),
        ("envelope", "Envelope"),
        ("ball", "Ball"),
        ("round", "Round"),
        ("log", "Log"),
        ("pat", "Pat"),
        ("fillet", "Fillet"),
        ("steak", "Steak"),
        ("rib", "Rib"),
        ("chop", "Chop"),
        ("drumstick", "Drumstick"),
        ("wing", "Wing"),
        ("thigh", "Thigh"),
        ("whole", "Whole"),
        ("quart", "Quart"),
        ("bundle", "Bundle"),
        ("slice", "Slice"),
        ("portion", "Portion"),
        ("serving", "Serving"),
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

    def __str__(self):
        return f"{self.name} ({self.category})"

class Instruction(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="instructions"
    )
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    time_minutes = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Estimated time for this step in minutes"
    )

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.description[:50]}"
    
class UserCookbook(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cookbook')
    recipes = models.ManyToManyField(Recipe, related_name='cookbooks')

@receiver(post_save, sender=User)
def create_user_cookbook(sender, instance, created, **kwargs):
    if created:
        UserCookbook.objects.create(user=instance)

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.user.username}'s Meal Plan starting {self.start_date}"
    
class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meals')
    recipe = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    servings = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.meal_type.capitalize()} on {self.date} - {self.recipe.title if self.recipe else 'No Recipe'}"