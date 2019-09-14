Welcome to GorillaML's documentation!
=====================================
This is the application which allow individual, organization, developer, publisher to manage, publish, monitor webservices, machine learning api, custom forms and many more things collaborately.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Installation
=====================================
.. code-block:: shell

    pip install gorillaml

DB Initialization
=====================================
After installation to initialized the application database we have to run below command in console.

.. code-block:: shell

    gorillaml-canvas init-db

.. warning:: Dont ignore or forget to run this command or else application stop working properly.

Start Application Server
=====================================
To start GorillaML server run below command in terminal

.. code-block:: shell

    gorillaml-start-server

It will expose the application in http://127.0.0.1:5000

Application Login
=====================================
Default username and password of the application is ``admin`` and ``admin``. After successfull login change your default
password as per your convenient time.