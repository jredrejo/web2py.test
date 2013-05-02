#!/usr/bin/env python

''' py.test configuration and fixtures file.

Tells application she's running in a test environment.
Creates a complete web2py environment, similar to web2py shell.
Creates a WebClient instance to browse your application, similar to a real
web browser.
Propagates some application data to test cases via fixtures, like baseurl and
automatic appname discovering.
'''

import os
import pytest
import sys

sys.path.insert(0, '')


@pytest.fixture(scope='module')
def baseurl(appname):
    '''The base url to call your application.

    Change you port number as necessary.
    '''

    return 'http://localhost:8000/%s/' % appname


@pytest.fixture(scope='module')
def appname():
    '''Discover application name.

    Your test scripts must be on applications/<your_app>/tests
    '''

    dirs = os.path.split(__file__)[0]
    appname = dirs.split(os.path.sep)[-2]
    return appname


@pytest.fixture(scope='module', autouse=True)
def fixture_create_testfile_to_application(request, appname):
    '''Creates a temp file to tell application she's running under a
    test environment.

    Usually you will want to create your database in memory to speed up
    your tests and not change your development database.

    This fixture is automatically run by py.test at module level. So, there's
    no overhad to test performance.
    '''

    # note: if you use Ubuntu, you can allocate your test database on ramdisk
    # simply using the /dev/shm directory.
    # There's no doubt a ramdisk is much faster than your harddisk, but use it
    # carefully if you don't have enough memory.
    temp_dir = '/dev/shm' # Ubuntu's native ramdisk is faster
    #temp_dir = '/tmp'

    # IMPORTANT: the temp_filename variable must have the same value as set in
    # your app/models/db.py file.
    temp_filename = '%s/tests_%s.tmp' % (temp_dir, appname)

    with open(temp_filename, 'w+') as tempfile:
        tempfile.write('aplicacao %s rodando em modo de teste' % appname)

    def _apaga_tempfile_que_identifica_o_teste():
        os.remove(temp_filename)
    request.addfinalizer(_apaga_tempfile_que_identifica_o_teste)


@pytest.fixture(autouse=True)
def fixture_cleanup_db(web2py):
    '''Truncate all database tables before every single test case.

    This can really slow down your tests. So, keep your test data small and try
    to allocate your database in memory.

    Automatically called by test.py due to decorator.
    '''

    for tab in web2py.db.tables:
        web2py.db[tab].truncate()
    web2py.db.commit()


@pytest.fixture(scope='module')
def client(baseurl, fixture_create_testfile_to_application):
    '''Create a new WebClient instance once per module.
    '''

    from gluon.contrib.webclient import WebClient
    webclient = WebClient(baseurl)
    return webclient


@pytest.fixture()
def web2py(appname, fixture_create_testfile_to_application):
    '''Create a Web2py environment similar to that achieved by
    Web2py shell.

    It allows you to use global Web2py objects like db, request, response,
    session, etc.

    Concerning tests, it is usually used to check if your database is an
    expected state, avoiding creating controllers and functions to help
    tests.
    '''

    from gluon.shell import env
    from gluon.storage import Storage

    web2py_env = env(appname, import_models=True,
                     extra_request=dict(is_local=True))

    # Uncomment next 2 lines to allow using global Web2py objects directly
    # in your test scripts.
    # del web2py_env['__file__']  # avoid py.test import error
    # globals().update(web2py_env)

    return Storage(web2py_env)
