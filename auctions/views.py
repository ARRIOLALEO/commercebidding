from django.contrib.auth import authenticate, login, logout, models
from django.db import IntegrityError
from django.forms import widgets
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Categories, Listings
from django import forms
from django.forms import NumberInput

def index(request):
    return render(request, "auctions/index.html")
categories_options = Categories()

class formadd(forms.Form):
    title = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'class':'form-control mb-1','placeholder':'Insert the name of the product'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control mb-1','placeholder':'Insert the desption of your product here'}))
    image = forms.FileField(required=False)
    price = forms.FloatField(required=False, min_value=0,
                             widget=NumberInput(attrs={'id': 'form_homework', 'step': '0.5', 'class':'form-control','placeholder':'add the price of the product'}))
    categories = forms.ChoiceField(choices=categories_options.get_cat())

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
        title = request.POST['title']
        description = request.POST['description']
        bet = request.POST['bet']
        image= request.POST['image']
        categorie = request.POST['categories']
        active = request.POST['isActive']
        item = Listings()
        item.title = title
        item.bit_start = bet
        item.save()
        return HttpResponse("imsending the form here")
    else:
        return render(request,"auctions/addlist.html",{'categories':list(Categories.objects.all()),'form':formadd})






