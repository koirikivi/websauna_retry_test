A tester for websauna retry support
===================================

Automatic retrying on Postgresl Serialization Errors seems to be broken for websauna.
This app is a hacky way to verify the issue.

Setup the app
-------------

    .. code-block:: shell

        python3 -m venv venv
        source venv/bin/activate
        pip install -U pip
        pip install -r requirements.txt
        createdb kaboom_dev
        ws-alembic -c my/app/conf/development.ini -x packages=all upgrade head


Run the app
-----------

    .. code-block:: shell

        pserve ws://my/app/conf/development.ini

Verify
------

1. Open http://localhost:6543/kaboom
2. Refresh the page a couple of times
3. If you see an internal server error each time, it is likely that retry support won't work correctly.
