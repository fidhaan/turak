from django.contrib import admin
from django.urls import path

from app.views import BalancesView, DeductOnlineView, DeductOfflineView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/balances/", BalancesView.as_view()),
    path("api/deduct/online/", DeductOnlineView.as_view()),
    path("api/deduct/offline/", DeductOfflineView.as_view()),
]