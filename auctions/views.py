from django.http import JsonResponse
from django import forms
from django.contrib.auth import authenticate, login, logout, models
from django.db import IntegrityError
from django.db.transaction import commit
from django.forms import ModelForm, fields, widgets
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Categories, bits, Listings
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
active = (("yes", "yes"), ("not", "not"))


def index(request):
    return render(request, "auctions/index.html", {"listings": Listings.objects.all()})


class formadd(ModelForm):
    def __init__(self, *args, **kwargs):
        super(formadd, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs = {
            "class": "input--style-4",
        }
        self.fields["description"].widget = forms.Textarea()
        self.fields["description"].widget.attrs = {"class": "input--style-4"}
        self.fields["bit_start"].widget.attrs = {
            "class": "input--style-4",
        }
        self.fields["image"].widget.attrs = {
            "class": "input--style-4",
        }
        self.fields["categorie"].widget.attrs = {
            "class": "input--style-4",
        }
        self.fields["is_active"].widget.attrs = {
            "class": "select2-selection__rendered input--style-4"
        }

    class Meta:
        model = Listings
        fields = [
            "title",
            "description",
            "image",
            "bit_start",
            "categorie",
            "is_active",
        ]


class makeabeat(ModelForm):
    class Meta:
        model = bits
        fields = ["bit"]


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def addlist(request):
    if request.method == "POST":
        form = formadd(request.POST, request.FILES)
        if form.is_valid():
            new_article = form.save()
            new_article.user = User.objects.get(id=request.user.id)
            new_article.save()
            return HttpResponseRedirect(reverse("index"))
        return HttpResponse("it was save")
    else:
        return render(request, "auctions/addlist.html", {"form": formadd})


@csrf_exempt
def see_list(request):
    if request.method == "POST":
        list_id = request.POST["id"]
        print(list_id)
        list = Listings.objects.get(id=list_id)
        print(list)
        owner = User.objects.get(username=list.user)
        offers = bits.objects.all().filter(listing_item=list.id).order_by("-bit")
        print(offers)
        return render(
            request,
            "auctions/seelist.html",
            {"list": list, "owner": owner.id, "makeabeat": makeabeat, "offers": offers},
        )
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def addoffer(request):
    if request.method == "POST":
        form = makeabeat(request.POST)
        if form.is_valid():
            newoffer = form.save()
            newoffer.user = User.objects.get(id=request.user.id)
            newoffer.listing_item = Listings.objects.get(id=request.POST["idlist"])
            newoffer.save()
            return HttpResponse("the offer was safe")
        return HttpResponse("we have some error")
    return HttpResponse(reverse("login"))



@login_required(login_url="/login")
def metrics(request):
    return render(request,"auctions/metrics.html") 

@login_required(login_url="/login")
def get_data_metrics(request,*args,**kwargs):
    products = serializers.serialize('json',Listings.objects.all().filter(user=request.user.id))
    return JsonResponse(products,safe=False)
