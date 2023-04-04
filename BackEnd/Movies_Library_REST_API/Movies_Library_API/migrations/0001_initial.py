# Generated by Django 4.1.7 on 2023-04-04 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
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
                ("title", models.CharField(max_length=100)),
                ("genre", models.CharField(max_length=100)),
                ("year", models.CharField(max_length=100)),
            ],
        ),
    ]
