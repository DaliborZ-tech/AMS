from django.contrib import admin
from django.urls import path

from app_sprava_montazi.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Mainview.as_view(), name="homepage"),
    path('login/', login_partial, name='login_partial'),

]
