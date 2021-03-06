# Generated by Django 3.2.3 on 2021-05-28 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_categories_listings"),
    ]

    operations = [
        migrations.CreateModel(
            name="Commentaries",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("the_comment", models.CharField(max_length=500)),
                (
                    "is_commentary_Active",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("Not", "Not")], max_length=3
                    ),
                ),
                (
                    "item_coment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auctions.listings",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="bits",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bit", models.FloatField()),
                (
                    "listing_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auctions.listings",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
