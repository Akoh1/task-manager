# task-manager
A web app to manage tasks

**Technology Used:** Django 2.0.6 (Python 3)

 **Database:** SQLite 3 (SQLite is used because it can be safely assumed that it would not be a very busy site and enterprise level database can be avoided)



## Installation

- Clone repository

    ```bash
    git clone git@gitlab.com:e4e-pycore/disc_personality_test.git
    ```
You'll need to have virtual enviroment installed on your machine

.. code-block:: sh

    pip3 install virtualenv


Setup virtual environment

.. code-block:: sh

    virtualenv -p python3 .virtualenv

Activate virtual environment

.. code-block:: sh

    source .virtualenv/bin/activate

    ```

- Install requirements

    ```bash
    pip install -r requirements.txt


Run migrations before starting the django-server

.. code-block:: sh

    python manage.py migrate
 To view the app append '/myapp' to the end of the localserver
	e.g 

