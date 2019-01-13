from django.contrib.sitemaps import Sitemap
from dtpmapapp.models import MVC, Region


class LimitSitemap(Sitemap):
    limit = 2000


class MVCSitemap(LimitSitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return MVC.objects.all()

    def lastmod(self, item):
        return item.created_at


class RegionSitemap(LimitSitemap):
    changefreq = "yearly"
    priority = 0.8

    def items(self):
        return Region.objects.all()

