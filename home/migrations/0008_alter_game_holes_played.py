# Generated by Django 5.0.1 on 2024-01-31 20:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_holescore"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="holes_played",
            field=models.CharField(max_length=64),
        ),
    ]
