from django.contrib import admin
from django.urls import include, path

from tasks.auth_views import RateLimitedLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "accounts/login/",
        RateLimitedLoginView.as_view(),
        name="login",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("tasks.urls", namespace="tasks")),
]
