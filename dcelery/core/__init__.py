from flask import Flask
from core import discovery
from core.extensions import db, babel


def create_app(settings):
    app = Flask("dcelery")
    app.config.from_object(settings)
    discovery.auto_discovery()
    # init sqlalchemy
    db.init_app(app)
    # init babel
    babel.init_app(app)

    return app
