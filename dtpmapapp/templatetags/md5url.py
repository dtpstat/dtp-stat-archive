import hashlib
import threading
from os import path
from django import template
from django.conf import settings

register = template.Library()


class UrlCache(object):
    _md5_sum = {}
    _lock = threading.Lock()

    @classmethod
    def get_md5(cls, file):
        try:
            return cls._md5_sum[file]
        except KeyError:
            with cls._lock:
                try:
                    for root_url in settings.STATICFILES_DIRS:
                        md5 = cls.calc_md5(path.join(root_url, file))[:8]
                        value = '%s%s?v=%s' % (settings.STATIC_URL, file, md5)
                except IsADirectoryError:
                    value = settings.STATIC_URL + file
                cls._md5_sum[file] = value
                return value

    @classmethod
    def calc_md5(cls, file_path):
        with open(file_path, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()


@register.simple_tag
def md5url(model_object):
    return UrlCache.get_md5(model_object)