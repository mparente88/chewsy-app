# This file and directory structure was provided entirely by ChatGPT 
# (at my request and prompting) for the purpose of creating dummy data 
# to test the app.

import random
from django.core.management.base import BaseCommand
from main_app.models import Recipe, Ingredient, Instruction, Tag, User

class Command(BaseCommand):
    help = 'Seed the database with random recipes for testing purposes'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database with recipes...")
        
        user = User.objects.first()  # Use the first user for all recipes
        if not user:
            self.stdout.write(self.style.ERROR("No users found. Create at least one user first."))
            return

        # Sample data
        recipe_titles = [
            "Spaghetti Bolognese", "Chicken Alfredo", "Vegetable Stir Fry", 
            "Beef Tacos", "Mushroom Risotto", "Grilled Cheese", "Caesar Salad", 
            "Tomato Soup", "BBQ Ribs", "Pancakes", "Waffles", "Chocolate Cake"
        ]
        ingredient_names = [
            "Chicken", "Beef", "Onion", "Garlic", "Tomato", "Salt", "Pepper",
            "Milk", "Cheese", "Flour", "Sugar", "Eggs", "Butter", "Rice", "Beans"
        ]
        instructions = [
            "Preheat the oven to 350°F.", "Chop all the vegetables.", 
            "Sauté the onions until golden.", "Add garlic and stir for 1 minute.",
            "Cook until the meat is browned.", "Simmer for 20 minutes.", 
            "Mix the ingredients together.", "Bake for 30 minutes."
        ]

        # Tags
        tag_names = [
            ("Quick", "time"), ("Easy", "complexity"), ("Healthy", "diet"),
            ("Italian", "cuisine"), ("Comfort Food", "taste"), ("Summer", "season")
        ]
        tags = []
        for tag_name, category in tag_names:
            tags.append(Tag.objects.get_or_create(name=tag_name, category=category)[0])

        # Seed recipes
        for _ in range(50):  # Adjust number of recipes to seed
            title = random.choice(recipe_titles) + f" {random.randint(1, 100)}"
            recipe = Recipe.objects.create(
                title=title,
                description=f"{title} is a delicious dish made with love.",
                user=user,
                prep_time=random.randint(5, 20),
                cook_time=random.randint(10, 50),
                servings=random.randint(1, 8),
            )
            
            # Add random tags
            recipe.tags.add(*random.sample(tags, random.randint(1, 3)))

            # Add random ingredients
            for _ in range(random.randint(3, 7)):
                Ingredient.objects.create(
                    recipe=recipe,
                    name=random.choice(ingredient_names),
                    quantity=random.randint(1, 5),
                    measurement=random.choice([m[0] for m in Ingredient.MEASUREMENT_CHOICES])
                )

            # Add random instructions
            for step_num, instruction_text in enumerate(random.sample(instructions, random.randint(3, 6)), start=1):
                Instruction.objects.create(
                    recipe=recipe,
                    step_number=step_num,
                    description=instruction_text
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database with test recipes."))
