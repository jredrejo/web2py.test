
An example of how to test an Web2py Application.

I use py.test [1] to test this application, but the concept can be applied in unittest and nose, too.

This work was done using Web2py v 2.4.5

IMPORTANT: I recommend you working with virtualenv to give you more freedom. It's not required, but highly recommended.

The very basic procedure is:
# create a new virtualenv (optional, but highly recommended). Let's call it web2py.test
# cd web2py.test
# source bin/activate
# pip install pytest (it will install py.test just in your virtualenv)
# download web2py stable [2]
# unzip web2py to your web2py.test/web2py dir
# clone this repo to web2py.test/web2py/applications/people subdir
# cd web2py (you must be in web2py root directory to run tests)
# py.test -x -v -s applications/people/tests
# voilà!


To understand the method used to allow run tests, refer to web2py/applications/people/tests/conftest.py

Read web2py/applications/people/models/db.py to see how to make your application know she is running under the test environment.

Test cases are in web2py/applications/people/tests subdirs.


Links used in this doc:

- [1] http://pytest.org
- [2] http://web2py.com/init/default/download
