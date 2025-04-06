from django.contrib import admin
from django.urls import path

from accounts.views import *
from app_sprava_montazi import views
from app_sprava_montazi.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Mainview.as_view(), name="homepage"),
    path('login_partial/', LoginPartialView.as_view(),
         name='login_partial'),
    path('ajax_login/', AjaxLoginView.as_view(), name='ajax_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("order_summary/", OrderSummaryView.as_view(),
         name="order_summary"),
    path('team-summary/', TeamSummaryView.as_view(),
         name='team_summary'),
    path("order-detail/<int:pk>/", OrderDetailView.as_view(),
         name="order_detail"),
    path("get-place-info/<str:zip_code>/", views.get_place_info,
         name="get_place_info"),




]
