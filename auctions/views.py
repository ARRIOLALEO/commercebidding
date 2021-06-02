from secrets import choice
from django.contrib.auth import authenticate, login, logout, models
from django.db import IntegrityError
from django.db.transaction import commit
from django.forms import fields, widgets
from django.forms.forms import Form
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


class formadd(forms.Form):
    title = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'class':'form-control mb-1','placeholder':'Insert the name of the product'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control mb-1','placeholder':'Insert the desption of your product here'}))
    image = forms.FileField(required=False)
    bit_start = forms.FloatField(required=False, min_value=0,
                             widget=NumberInput(attrs={'id': 'form_homework', 'step': '0.5', 'class':'form-control','placeholder':'add the price of the product'}))
    categorie = forms.ModelChoiceField(queryset=Categories.objects.all(),empty_label="Select the Categorie",widget=forms.Select(attrs={'class':'form-control'}))
    is_active= forms.ChoiceField(choices=active,widget=forms.Select(attrs={'class':'form-control'}))

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
            title= form.cleaned_data['title']
            categorie = form.cleaned_data['categorie']
            price = form.cleaned_data['bit_start']
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            new_list = Listings()
            new_list.title = title
            new_list.bit_start = price
            new_list.image = image
            new_list.description = description
            new_list.save()
            new_list.categorie.set(categorie)
            new_list.save()
            return HttpResponse("this was not save")
        return HttpResponse("it was save")
    else:
        return render(request,"auctions/addlist.html",{'form':formadd})






