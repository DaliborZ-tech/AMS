from django.shortcuts import render
from django.views.generic import TemplateView


class Mainview(TemplateView):
    template_name = "app_sprava_montazi.html"


