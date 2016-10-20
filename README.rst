Somarket
========

Social Accounts auction

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django



Basic Commands
--------------

Upgrade your pip requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    $ pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd somarket
    celery -A somarket.taskapp worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.


Deployment
----------

Docker
^^^^^^
.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


