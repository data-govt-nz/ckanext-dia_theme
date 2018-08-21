=============
ckanext-dia_theme
=============

Frontend CKAN theme for data.govt.nz written in LESS

------------
Requirements
------------

CKAN 2.7.x

------------
Installation
------------

To install ckanext-dia_theme:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-dia_theme Python package into your virtual environment::

     pip install ckanext-dia_theme

3. Add ``dia_theme`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Nginx on Ubuntu::

     sudo service nginx restart


---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    #TODO - provide config values
    ckanext.dia_theme.some_setting = some_default_value


------------------------
Development Installation
------------------------

To install ckanext-dia_theme for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/data-govt-nz/ckanext-dia_theme.git
    cd ckanext-dia_theme
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.dia_theme --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-dia_theme on PyPI
---------------------------------

ckanext-dia_theme should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-dia_theme. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-dia_theme
----------------------------------------

ckanext-dia_theme is availabe on PyPI as https://pypi.python.org/pypi/ckanext-dia_theme.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags

       
----------------------------------------
CSS Styling of dia_theme
----------------------------------------

Any CSS styling changes to the dia_theme should be done in the LESS files and NOT directly in the CSS files.

Follow these steps:

 - Install LESS Compiler
 - Make changes in LESS files as required
 - Open console and cd to /path/to/ckanext-dia_theme
 - Compile the LESS files by running " lessc less/main.less fanstatic/dia_custom.css "
 - The CSS changes will now show up in the browser
 
