# Generated by Django 3.2.3 on 2021-06-07 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_listings_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bits",
            name="listing_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="auctions.listings",
            ),
        ),
        migrations.AlterField(
            model_name="bits",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]