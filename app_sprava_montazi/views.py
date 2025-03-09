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
        # Základní queryset všech zakázek (seřazený od nejnovější)
        orders_qs = Order.objects.all().select_related('store', 'place', 'team', 'status').order_by('-created')
        # Aplikace filtrů podle GET parametrů:
        order_no = self.request.GET.get('order_number')
        if order_no:
            orders_qs = orders_qs.filter(order_number__icontains=order_no)
        mandant = self.request.GET.get('mandant')
        if mandant:
            orders_qs = orders_qs.filter(mandant__icontains=mandant)
        store_id = self.request.GET.get('store')
        if store_id:
            orders_qs = orders_qs.filter(store_id=store_id)
        team_id = self.request.GET.get('team')
        if team_id:
            orders_qs = orders_qs.filter(team_id=team_id)
        start_date = self.request.GET.get('evidence_start')
        end_date = self.request.GET.get('evidence_end')
        if start_date or end_date:
            # filtr podle zadaného období evidence
            if start_date and end_date:
                orders_qs = orders_qs.filter(evidence_term__range=[start_date, end_date])
            elif start_date:
                orders_qs = orders_qs.filter(evidence_term__gte=start_date)
            elif end_date:
                orders_qs = orders_qs.filter(evidence_term__lte=end_date)
        # Stránkování (10 záznamů na stránku)
        paginator = Paginator(orders_qs, 10)
        page_number = self.request.GET.get('page', 1)
        try:
            orders_page = paginator.page(page_number)
        except PageNotAnInteger:
            orders_page = paginator.page(1)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)
        context['orders'] = orders_page
        # Předat seznamy pro dropdown filtry
        context['stores'] = Store.objects.all()
        context['teams'] = Team.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, self.template_name, context)
        else:
            # Vrácení celé stránky, pokud nejde o AJAX požadavek.
            return render(request, "partials/order_summary.html",
                          context)



