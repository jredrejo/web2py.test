# -*- coding: utf-8 -*-

# note: if you use Ubuntu, you can allocate your test database on ramdisk
# simply using the /dev/shm directory.
# There's no doubt a ramdisk is much faster than your harddisk, but use it
# carefully if you don't have enough memory.
temp_dir = '/dev/shm' # Ubuntu's native ramdisk is faster
#temp_dir = '/tmp'


def _i_am_running_under_tests():
    '''Check if Web2py is running under a test environment.
    '''

    test_running = False
    if request.is_local:
        # IMPORTANT: the temp_filename variable must be the same as the one set
        # on your tests/conftest.py file.
        temp_filename = '%s/tests_%s.tmp' % (temp_dir, request.application)

        import glob
        if glob.glob(temp_filename):
            test_running = True

    return test_running


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    if _i_am_running_under_tests():
        db = DAL('sqlite://test_storage.sqlite', folder=temp_dir)
    else:
        db = DAL('sqlite://storage.sqlite', pool_size=1, check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))



## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
