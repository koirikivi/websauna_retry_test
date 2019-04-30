A tester for websauna retry support
===================================

Automatic retrying on PostgreSQL Serialization Errors (TransactionRollback) seems to be broken for Websauna.
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

Fix
---

    .. code-block:: shell

        pip uninstall websauna
        pip install -e "git+https://github.com/koirikivi/websauna.git@fix-view-retrying#egg=websauna"

Then, restart the development server (`pserve`) and follow the steps in
"Verify" again. You should still occassionally see the internal server error
view, but most request should now not result in that view.
