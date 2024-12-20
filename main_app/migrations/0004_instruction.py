# Generated by Django 5.1.4 on 2024-12-10 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_remove_recipe_total_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('time_minutes', models.PositiveIntegerField(blank=True, help_text='Estimated time for this step in minutes', null=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructions', to='main_app.recipe')),
            ],
            options={
                'ordering': ['step_number'],
            },
        ),
    ]
