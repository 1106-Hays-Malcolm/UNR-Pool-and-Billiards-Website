# Generated by Django 5.1.7 on 2025-03-31 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0008_alter_game_options_alter_rating_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'permissions': [('can_view_others_ratings', 'Can view the ratings of other players. This permission is required to view the registry.')]},
        ),
    ]
