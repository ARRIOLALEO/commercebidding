# Generated by Django 3.2.3 on 2021-06-03 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listings_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='image',
            field=models.FileField(upload_to='media'),
        ),
    ]
