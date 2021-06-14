from django.contrib.auth import logout
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("social_django.urls")),
    path("logout", views.logout_view, name="logout"),
    path("addlist", views.addlist, name="addlist"),
    path("seelist/<int:product>/", views.see_list, name="seelist"),
    path("addoffer", views.addoffer, name="addoffer"),
    path("usermetrics", views.metrics, name="usermetrics"),
    path("getdata", views.get_data_metrics, name="getdata"),
    path("seecategorie", views.seecategorie, name="seecategorie"),
]
