from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class Mainview(TemplateView):
    template_name = "app_sprava_montazi.html"
