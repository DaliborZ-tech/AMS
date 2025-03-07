from django.shortcuts import render
from django.views.generic import TemplateView

from app_sprava_montazi.forms import LoginForm


# Create your views here.
class Mainview(TemplateView):
    template_name = "app_sprava_montazi.html"


def login_partial(request):
    form = LoginForm()
    return render(request, 'partials/login_form.html', {'form': form})


