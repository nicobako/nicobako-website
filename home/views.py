from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import NewUserForm

from typing import Any, Dict

# Create your views here.
class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["social_media_links"] = []

        def create_social_media_link(static_img:str, link:str):
            return {"static_img":f"home/images/{static_img}", "link":link}

        context["social_media_links"].append(
            create_social_media_link(
                static_img="github-logo.png",
                link="https://github.com/nicobako",
            )
        )

        context["social_media_links"].append(
            create_social_media_link(
                static_img="linkedin-logo.png",
                link="https://linkedin.com/in/nicobako",
            )
        )
        return context

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_user(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="home/register.html",
        context={"register_form": form},
    )


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login_user(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("home:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="home/login.html", context={"login_form": form}
    )


def logout(request):
    logout_user(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home:index")
