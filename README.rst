=============
ckanext-dia_theme
=============

Frontend CKAN theme for data.govt.nz written in LESS

------------
Requirements
------------

CKAN 2.9.x or 2.10.x

If using CKAN 2.8.x, checkout this repo at tag 3.2.0
If using CKAN 2.7.x, checkout this repo at tag 2.1.1

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


----------------------------------------
CSS Styling of dia_theme
----------------------------------------

Any CSS styling changes to the dia_theme should be done in the LESS files and NOT directly in the CSS files.

We'll be replacing these styles with the rua pattern library, however for now we have both.

You can use npm to install and build the LESS files with `npm i` and `npm run css`

If you are actively developing/making css changes you can run `npm run css-dev` and the .less files will be automatically compiled on save.

You can use npm to update the rua pattern library styles with `npm run rua`

Alternatively the LESS files were previously compiled with these steps:

 - Install LESS Compiler
 - Make changes in LESS files as required
 - Open console and cd to /path/to/ckanext-dia_theme
 - Compile the LESS files by running " lessc less/main.less fanstatic/dia_custom.css "
 - The CSS changes will now show up in the browser

