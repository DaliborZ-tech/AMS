from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import TemplateView

from accounts.forms import LoginForm


class LoginPartialView(TemplateView):
    template_name = 'partials/login_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context


class AjaxLoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False,
                                     'error': 'Nesprávné přihlašovací údaje!'})
        return JsonResponse({'success': False, 'error': 'Neplatný formulář'})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({"success": True})
