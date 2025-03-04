from django.contrib import admin
from django.urls import path

from app_sprava_montazi.views import Mainview

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Mainview.as_view(), name="homepage"),
]
