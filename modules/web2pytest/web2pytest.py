#!/usr/bin/env python

"""Infrastructure to run an Web2py application under test environment.

We create a temporary file to indicate the application she's running
under test.

By default this file is created in ramdisk (Ubuntu) to speed up
execution.

Web2py applications need this external injection mainly to know
where to create their test database.

Note: if you don't use webclient interface to run your tests, you don't
need to use this module.
"""

import glob
import os

#default_path = "/tmp"
default_path = "/dev/shm/web2py_test" # Ubuntu native ramdisk is faster
default_filename = "web2py_test_indicator"

_test_filename = None


def testfile_name(path=None, filename=None):
    global _test_filename
    if _test_filename and not (path or filename):
        return _test_filename

    path = path if path is not None else default_path
    filename = filename if filename is not None else default_filename
    _test_filename = os.path.join(path, filename)

    return _test_filename


def create_testfile(path=None, filename=None):
    """Creates a temp file to tell application she's running under a
    test environment.
    """

    fname = testfile_name(path, filename)

    try:
        os.mkdir(os.path.dirname(fname))
    except OSError as e:
        pass

    try:
        with open(fname, "w+") as f:
            f.write("web2py running in test mode.")
        return True
    except:
        return False


def delete_testfile():
    try:
        os.remove(testfile_name())
        return True
    except:
        return False


def testfile_exists(path=None, filename=None):
    fname = testfile_name(path, filename)

    try:
        if glob.glob(fname):
            return True
        else:
            return False
    except:
        return False


def is_running_under_test(request=None):
    request = request if request is not None else {}

    if request.get('_running_under_test') or testfile_exists():
        return True
    else:
        return False

def is_running_webclient():
    return testfile_exists()