from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import TemplateView
from app_sprava_montazi.models import *


class Mainview(TemplateView):
    template_name = "app_sprava_montazi.html"


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'partials/dashboard.html'


class OrderSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'partials/order_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all().order_by('-created')
        paginator = Paginator(orders, 10)  # počet položek na stránku

        page_number = self.request.GET.get('page', 1)
        try:
            orders_page = paginator.page(page_number)
        except PageNotAnInteger:
            orders_page = paginator.page(1)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)

        context['orders'] = orders_page
        return context

