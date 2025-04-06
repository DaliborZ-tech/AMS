from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView
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
        if self.request.GET.get('open'):
            orders_qs = orders_qs.filter(status__status__in=["New", "Adviced"])
        if self.request.GET.get('realized'):
            orders_qs = orders_qs.filter(status__status__in=["Realized"])
        if self.request.GET.get('canceled'):
            orders_qs = orders_qs.filter(status__status__in=["Canceled"])
        if self.request.GET.get('billed'):
            orders_qs = orders_qs.filter(status__status__in=["Billed"])
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
        paginator = Paginator(orders_qs, 50)
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


class TeamSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'partials/team_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams_qs = Team.objects.all().order_by('company')

        # Aplikace filtrů podle GET parametrů:
        company = self.request.GET.get('company')
        if company:
            teams_qs = teams_qs.filter(company__icontains=company)
        city = self.request.GET.get('city')
        if city:
            teams_qs = teams_qs.filter(city__icontains=city)
        active = self.request.GET.get('active')
        if active:
            if active.lower() == 'true':
                teams_qs = teams_qs.filter(active=True)
            elif active.lower() == 'false':
                teams_qs = teams_qs.filter(active=False)

        # Stránkování (50 záznamů na stránku)
        paginator = Paginator(teams_qs, 50)
        page_number = self.request.GET.get('page', 1)
        try:
            teams_page = paginator.page(page_number)
        except PageNotAnInteger:
            teams_page = paginator.page(1)
        except EmptyPage:
            teams_page = paginator.page(paginator.num_pages)
        context['teams'] = teams_page

        # Předání seznamu pro dropdown filtry – unikátní hodnoty pro společnosti a města
        context['companies'] = Team.objects.values_list('company',
                                                        flat=True).distinct()
        context['cities'] = Team.objects.values_list('city',
                                                     flat=True).distinct()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, context)


class OrderDetailView(DetailView):
    model = Order
    template_name = "partials/order_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.headers.get("HX-Request"):
            return HttpResponse(
                render_to_string(self.template_name, context, request=request))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.customer_name = request.POST.get("customer_name",
                                                     self.object.customer_name)

        # upravit contact
        contact = self.object.contact
        if contact is None:
            contact = Contact()
            self.object.contact = contact

        street_data = request.POST.get("street", "").split(maxsplit=1)
        if len(street_data) == 2:
            contact.street, contact.number = street_data
        else:
            contact.street = street_data[0]
            contact.number = ""

        contact.phone = request.POST.get("phone", contact.phone)
        contact.email = request.POST.get("email", contact.email)

        contact.save()
        self.object.save()

        # správně připravit kontext pomocí self.object
        context = self.get_context_data(object=self.object)

        if request.headers.get("HX-Request"):
            html = render_to_string(self.template_name, context,
                                    request=request)
            return HttpResponse(html)

        return super().post(request, *args, **kwargs)
