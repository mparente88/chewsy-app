# Generated by Django 5.1.4 on 2024-12-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_mealplan_meal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
