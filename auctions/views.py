from secrets import choice
from django.contrib.auth import authenticate, login, logout, models
from django.db import IntegrityError
from django.db.transaction import commit
from django.forms import fields, widgets
from django.forms.forms import Form
from  django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Categories, Listings
from django import forms
from django.forms import NumberInput

active = (('yes','yes'),('not','not'))

def index(request):
    return render(request, "auctions/index.html")


class formadd(ModelForm):
    class Meta:
        model = Listings
        fields =['title','description','bit_start','categorie','is_active']

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def addlist(request):
    if request.method =="POST":
        form = formadd(request.POST)
        if form.is_valid():
            new_article = form.save()
            return HttpResponse("this was ok all")
        return HttpResponse("it was save")
    else:
        return render(request,"auctions/addlist.html",{'form':formadd})






