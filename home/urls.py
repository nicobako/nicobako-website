from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("register", view=views.register, name="register"),
    path("login", view=views.login, name="login"),
    path("logout", view=views.logout, name="logout"),
]
