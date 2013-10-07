
An example of how to test an Web2py Application.

I use py.test [1] to test this application, but the concept can be applied in unittest and nose, too.

Tested in Web2py v2.4.5

IMPORTANT: I recommend you work with virtualenv to give you more freedom. It's not required, but strongly recommended.

The procedure to run tests present for this application is:

1. create a new virtualenv. Let's call it web2py.test
1. $ cd web2py.test
1. $ source bin/activate
1. $ pip install pytest (it will install py.test just in your virtualenv)
1. download web2py stable [2]
1. unzip web2py to your web2py.test/web2py dir
1. clone this repo to web2py.test/web2py/applications/people subdir
1. $ cd web2py (you must be in web2py root directory to run tests)
1. $ python web2py.py -a my_password --nogui &
1. $ py.test -x -v -s applications/people/tests

Voilà!

To understand the method used to allow run tests, refer to web2py/applications/people/tests/conftest.py

Read web2py/applications/people/models/db.py to see how to make your application know she is running under the test environment.

Test cases are in web2py/applications/people/tests subdirs.


There are 3 important parts in this application:

1. tests/conftest.py -> configure test environment.
1. modules/web2pytest/web2pytest.py -> test infrastructure.
1. models/db.py -> ask web2pytest about tests and create db accordingly.


Links used in this doc:

- [1] http://pytest.org
- [2] http://web2py.com/init/default/download
