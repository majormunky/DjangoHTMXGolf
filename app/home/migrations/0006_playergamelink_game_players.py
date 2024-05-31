# Generated by Django 5.0.1 on 2024-01-29 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0005_player"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerGameLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.game"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.player"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="game",
            name="players",
            field=models.ManyToManyField(
                through="home.PlayerGameLink", to="home.player"
            ),
        ),
    ]