"""
Django middleware for generating request flame graphs.
Requires the flamegraph.pl perl script:
https://github.com/brendangregg/FlameGraph/blob/master/flamegraph.pl
Installation:
1. Create a directory for flame graphs
2. Copy the flamegraph.pl script to it
3. Add the FLAMES_DIR django setting
4. Add the flames.FlamesMiddleware to MIDDLEWARE_CLASSES
Usage:
To generate a flame graph just append ?flames to the requested url.
Middleware will create an svg in the FLAMES_DIR with the current timestamp.
Uncomment line 88 to automatically open the svg in a new google chrome tab.
"""

import os
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime
from xml.dom.minidom import Text

from django.conf import settings

FLAMES_DIR = os.path.abspath(settings.FLAMES_DIR)


def get_module_name(module_path):
    for path in sys.path:
        path = path or os.getcwd()

        if module_path.startswith(path):
            rel_path = module_path[len(path) + 1:]

            return (
                rel_path
                .replace(u'/__init__.py', u'')
                .replace(u'/', '.')
                .replace(u'.py', u'')
                .strip()
            )

    return module_path


def write_samples(file, samples):
    for _, frame in samples:
        stack = traceback.extract_stack(frame)
        frame_strings = (
            func_name + u'@' + get_module_name(module_path)
            for module_path, _, func_name, _ in stack
        )
        stack_string = u';'.join(frame_strings)
        file.write(u'{} {}\n'.format(stack_string, 1))


def write_flames(logger, title='flames'):
    base_path = os.path.join(
        FLAMES_DIR,
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
    )

    out_txt_path = base_path + '.txt'
    out_svg_path = base_path + '.svg'

    title_element = Text()
    title_element.data = title
    title_xml = title_element.toxml()

    with open(out_txt_path, 'w') as out_txt:
        write_samples(out_txt, logger.samples)


class StackLogger(object):
    def __init__(self, thread_id, interval=0.001):
        super(StackLogger, self).__init__()

        self.thread_id = thread_id
        self.interval = interval
        self.should_stop = False
        self.samples = []

        self.started = threading.Event()
        self.thread = threading.Thread(target=self.run)

    def run(self):
        start_time = time.time()
        self.samples = []
        self.started.set()

        while not self.should_stop:
            frame_start = time.clock()

            timestamp = time.time() - start_time
            frame = sys._current_frames()[self.thread_id]
            self.samples.append((timestamp, frame))

            frame_dt = time.clock() - frame_start
            time.sleep(max(0, self.interval - frame_dt))

    def start(self):
        self.started.clear()
        self.should_stop = False
        self.thread.start()
        self.started.wait()

    def stop(self):
        self.should_stop = True
        self.thread.join()


class FlamesMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG and 'flames' in request.GET:
            logger = StackLogger(threading.current_thread().ident)
            logger.start()
            request._stack_logger = logger

        response = self.get_response(request)

        if settings.DEBUG and hasattr(request, '_stack_logger'):
            logger = request._stack_logger
            logger.stop()

            url = request.build_absolute_uri()
            write_flames(logger, title=url)

        return response