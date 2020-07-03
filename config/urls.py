"""Mad Libz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.conf import settings
from django.urls import include, path

from django.conf.urls.static import static

urlpatterns = [
    path(r"health-check/", include("health_check.urls")),
    path(r"auth/", include("gatekeeper.urls")),
    path("", include("mad_libz.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # Add view for Django settings
    from config import debug

    urlpatterns += [path(r"_debug_info/", debug.splode)]

    # Add views to debug error templates
    import django.views.defaults

    urlpatterns += [
        path(r"_debug_404/", django.views.defaults.page_not_found),
        path(r"_debug_500/", django.views.defaults.server_error),
        path(r"_debug_400/", django.views.defaults.bad_request),
        path(r"_debug_403/", django.views.defaults.permission_denied),
    ]

    # Add static files URL
    import django.contrib.staticfiles.urls

    urlpatterns += django.contrib.staticfiles.urls.urlpatterns
