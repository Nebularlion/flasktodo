import os

from flask import Flask


def create_app(test_config = None):

    # creates the FLask instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flasktodo.sqlite'),
    )

    if test_config is None:
        # loads the instance config
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.update(test_config)

    # ensures the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database command
    from flasktodo import db
    db.init_app(app)

    # apply the blueprints to the app
    from flasktodo import auth, todolist
    app.register_blueprint(auth.bp)
    app.register_blueprint(todolist.bp)

    app.add_url_rule('/', endpoint='index')

    return app
