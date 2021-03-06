from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices


class User(AbstractUser):
    pass


class Categories(models.Model):
    name_cat = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name_cat}"

    def get_cat(self):
        return f"{self.name_cat}"


class Listings(models.Model):
    list_active = [("not", "yes"), ("not", "not")]
    title = models.CharField(max_length=160)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="media/%Y/%m/%d/", blank=True)
    bit_start = models.FloatField()
    categorie = models.ManyToManyField(Categories, related_name="categories")
    is_active = models.CharField(max_length=8, choices=list_active)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class bits(models.Model):
    bit = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing_item = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)


class Commentaries(models.Model):
    is_active = [("Yes", "Yes"), ("Not", "Not")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_coment = models.ForeignKey(Listings, on_delete=models.CASCADE)
    the_comment = models.CharField(max_length=500)
    is_commentary_Active = models.CharField(max_length=3, choices=is_active)
