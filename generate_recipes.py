# This code was provided by ChatGPT at my request to seed the Heroku Database

import random
from main_app.models import Recipe, Ingredient, Instruction, Tag, User

# Fetch all users and tags
users = list(User.objects.all())
tags = list(Tag.objects.all())

# Define dummy data
titles = ["Spaghetti", "Tacos", "Salad", "Soup", "Pancakes", "Burger", "Curry", "Pizza", "Steak", "Sandwich"]
descriptions = [
    "A delicious meal to brighten your day.",
    "Quick and easy, perfect for a busy schedule.",
    "A hearty recipe packed with flavor.",
    "Simple to make and loved by all.",
    "Perfect for breakfast, lunch, or dinner."
]
ingredients = ["Flour", "Sugar", "Salt", "Butter", "Eggs", "Tomatoes", "Chicken", "Cheese", "Beef", "Rice", "Milk", "Onions"]
measurements = [choice[0] for choice in Ingredient.MEASUREMENT_CHOICES]
instructions = [
    "Mix all ingredients in a bowl.",
    "Cook on medium heat until done.",
    "Add seasoning to taste.",
    "Bake in the oven at 350°F for 30 minutes.",
    "Serve hot and enjoy!"
]

# Generate 500 recipes
for i in range(500):
    # Select a random user
    user = random.choice(users)

    # Create a new recipe
    recipe = Recipe.objects.create(
        title=f"{random.choice(titles)} {i + 1}",
        description=random.choice(descriptions),
        user=user,
        prep_time=random.randint(5, 60),
        cook_time=random.randint(10, 120),
        servings=random.randint(1, 8),
    )

    # Add random tags (1-3 per recipe)
    recipe.tags.set(random.sample(tags, k=random.randint(1, min(3, len(tags)))))

    # Add random ingredients (3-6 per recipe)
    for j in range(random.randint(3, 6)):
        Ingredient.objects.create(
            recipe=recipe,
            name=random.choice(ingredients),
            quantity=random.randint(1, 10),
            measurement=random.choice(measurements),
            order=j + 1
        )

    # Add random instructions (3-5 steps per recipe)
    for j in range(random.randint(3, 5)):
        Instruction.objects.create(
            recipe=recipe,
            step_number=j + 1,
            description=f"Step {j + 1}: {random.choice(instructions)}",
            time_minutes=random.randint(2, 15) if random.random() > 0.5 else None
        )

    # Print progress every 50 recipes
    if (i + 1) % 50 == 0:
        print(f"{i + 1} recipes created.")

print("500 recipes with ingredients and instructions created successfully!")
