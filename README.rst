Welcome to GorillaML's documentation!
=====================================
This is the analytical tools which allow individual, organization, developer, publisher to present, manage, publish their architectural design, machine learning api, custom form builder for input data capturing, live code editor and many more active development very easily.

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

Start Application in Desktop
=====================================
If it is installed on personal desktop based environment then to start GorillaML server, run below command in terminal..

.. code-block:: shell

    gorillaml-canvas gui

Start Application Server in private cloud
=====================================
To start GorillaML server run below command in terminal

.. code-block:: shell

    gorillaml-canvas start-forever

It will expose the application in http://localhost:5000

Application Login
=====================================
Default username and password of the application is ``admin`` and ``admin``. After successfull login change your default
password as per your convenient time.

Plugin Development
=====================================
GorillaML is created on top of Flask framework and this plugins are created based on Flask blueprint framework. You have full controll to play with gorillaml plugins using Flask blueprint for more details start reading https://flask.palletsprojects.com/en/1.1.x/blueprints/

You will found sample plugins here https://github.com/washim/GorillaML_Plugins

.. warning:: Plugin name and blueprint name should be same inside plugin.py. This **plugin.py** and **__init__.py** is the mandatory to create gorillaml plugins. Dont change **gorillaml** variable inside plugin.py
