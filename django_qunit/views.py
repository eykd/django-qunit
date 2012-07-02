from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.utils import simplejson

import os


def get_suite_context(request, path):
    full_path = os.path.join(settings.QUNIT_TEST_DIRECTORY, path)
    full_path, directories, files = os.walk(full_path).next()

    suite = {}

    # set suite name
    pieces = path.split('/')
    if len(pieces) < 2:
        suite['name'] = 'main'
    else:
        suite['name'] = ''.join(pieces[-2])

    # defaults
    suite['extra_urls'] = []
    suite['extra_media_urls'] = []
    suite['extra_static_urls'] = []

    # load suite.json if present
    if 'suite.json' in files:
        with open(os.path.join(full_path, 'suite.json'), 'r') as fi:
            json = fi.read()
        suite.update(simplejson.loads(json))

    previous_directory = parent_directory(path)

    return {
        'files': [path + f for f in files if f.endswith('js')],
        'previous_directory': previous_directory,
        'in_subdirectory': previous_directory is not None,
        'subsuites': directories,
        'suite': suite,
    }


def run_tests(request, path):
    suite_context = get_suite_context(request, path)
    return render_to_response('qunit/index.html', suite_context,
                              context_instance=RequestContext(request))


def parent_directory(path):
    """
    Get parent directory. If root, return None
    "" => None
    "foo/" => "/"
    "foo/bar/" => "foo/"
    """
    if path == '':
        return None
    prefix = '/'.join(path.split('/')[:-2])
    if prefix != '':
        prefix += '/'
    print path, '->', prefix
    return prefix
