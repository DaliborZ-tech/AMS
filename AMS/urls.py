from django.contrib import admin
from django.urls import path

from accounts.views import *
from app_sprava_montazi.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Mainview.as_view(), name="homepage"),
    path('login_partial/', LoginPartialView.as_view(),
         name='login_partial'),
    path('ajax_login/', AjaxLoginView.as_view(), name='ajax_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),


]
