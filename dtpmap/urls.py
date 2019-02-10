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
from django.conf.urls import url
from django.http import HttpResponse
from django.contrib import admin

from dtpmap import settings
from dtpmapapp import views
from django.contrib.sitemaps import views as sitemapviews
from django.views.decorators.cache import cache_page
from dtpmapapp.sitemaps import *

sitemaps = {
    'mvcs': MVCSitemap(),
    'regions': RegionSitemap()
}

urlpatterns = [

    url(r'^sitemap\.xml$', sitemapviews.index, {'sitemaps': sitemaps}),
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(24 * 60 * 60)(sitemapviews.sitemap),
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    url(r'^admin1/', admin.site.urls),
    url(r'^about/', views.about, name='about'),
    url(r'^api/regions/(?P<region_alias>[-_\w]+)/mvcs/$', views.mvcs_by_region, name='mvc by region'),
    url(r'^api/regions/(?P<region_alias>[-_\w]+)/areas/(?P<area_alias>[-_\w]+)/mvcs/$', views.mvcs_by_area,
        name='mvc by area'),
    url(r'^api/dicts/$', views.dicts, name='dictionaries'),
    url(r'^api/participant_types/$', views.participant_types, name='participant_types'),
    url(r'^api/search_region/$', views.search_region, name='search region'),
    url(r'^$', views.home, name='home'),
    url(r'^(?P<region_alias>[-_\w]+)/$', views.region, name='region page'),
    url(r'^dtp/(?P<mvc_alias>[-_\w]+)/$', views.mvc, name='mvc page'),
]


def robots_file(x):
    return HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain")


if settings.DEBUG:
    urlpatterns.append(url(r'^robots.txt', robots_file, name="robots_file"))
