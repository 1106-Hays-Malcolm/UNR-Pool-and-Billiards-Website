# Generated by Django 5.1.7 on 2025-03-30 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0006_alter_rating_rating_alter_rating_rating_deviation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='ranked',
            field=models.BooleanField(default=True),
        ),
    ]
