"""dtpmap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps import views as sitemapviews
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page

from dtpmapapp import views
from dtpmapapp.sitemaps import *

sitemaps = {"mvcs": MVCSitemap(), "regions": RegionSitemap()}


urlpatterns = [
    path("sitemap.xml", sitemapviews.index, {"sitemaps": sitemaps}),
    re_path(
        r"^sitemap-(?P<section>.+)\.xml$",
        cache_page(24 * 60 * 60)(sitemapviews.sitemap),
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("admin1/", admin.site.urls),
    path("about/", views.about, name="about"),
    path("api/v1/", include(("api.v1.urls", "api_v1"))),
    re_path(
        r"^api/regions/(?P<region_alias>[-_\w]+)/mvcs/$",
        views.mvcs_by_region,
        name="mvc by region",
    ),
    re_path(
        r"^api/regions/(?P<region_alias>[-_\w]+)/areas/(?P<area_alias>[-_\w]+)/mvcs/$",
        views.mvcs_by_area,
        name="mvc by area",
    ),
    path("^api/dicts/", views.dicts, name="dictionaries"),
    path("api/participant_types/", views.participant_types, name="participant_types"),
    path("api/search_region/", views.search_region, name="search region"),
    path("", views.home, name="home"),
    re_path(r"^(?P<region_alias>[-_\w]+)/$", views.region, name="region page"),
    re_path(r"^dtp/(?P<mvc_alias>[-_\w]+)/$", views.mvc, name="mvc page"),
]
