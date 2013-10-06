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

import os

#default_dirname = "/tmp"
default_dirname = "/dev/shm/web2py_test" # Ubuntu native ramdisk is faster
default_filename = "web2py_test_indicator"

test_filename = None


def create_testfile(dirname=None, filename=None):
    """Creates a temp file to tell application she's running under a
    test environment.
    """

    dirname = dirname or default_dirname
    filename = filename or default_filename
    test_filename = "%s/%s.tmp" % (dirname, filename)

    os.mkdir(dirname)

    with open(test_filename, "w+") as f:
        f.write("web2py running in test mode.")


def delete_testfile():
    os.remove(test_filename)
