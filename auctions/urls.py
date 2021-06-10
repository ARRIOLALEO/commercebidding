from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlist", views.addlist, name="addlist"),
    path("seelist", views.see_list, name="seelist"),
    path("addoffer", views.addoffer, name="addoffer"),
    path("usermetrics", views.metrics, name="usermetrics"),
    path("getdata", views.get_data_metrics, name="getdata"),
]
