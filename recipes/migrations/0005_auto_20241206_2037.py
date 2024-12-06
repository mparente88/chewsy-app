from django.db import migrations

def create_initial_data(apps, schema_editor):
    Category = apps.get_model('recipes', 'Category')
    Tag = apps.get_model('recipes', 'Tag')

    categories = [
        "Appetizer/Starter",
        "Main Course",
        "Side Dish",
        "Salad",
        "Soup/Stew",
        "Breakfast/Brunch",
        "Dessert",
        "Beverage",
        "Bread/Baked Good",
        "Sauce/Spread/Dip"
    ]

    for c in categories:
        Category.objects.get_or_create(name=c)

    tags = [
        "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free", "Low Carb",
        
        "Italian", "Mexican", "Chinese", "Indian", "Mediterranean", "American",
        
        "Grilled", "Roasted", "Fried", "Steamed", "Raw",
        
        "Spicy", "Sweet", "Savory",
        
        "Quick (under 30 mins)", "Intermediate (30-60 mins)", "Complex (over 60 mins)",
        
        "Kid-Friendly", "Holiday-Special", "Comfort-Food", "Summer", "Winter", "Fall", "Spring", "Picnic-Ready"
    ]

    for t in tags:
        Tag.objects.get_or_create(name=t)

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_category_name'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
