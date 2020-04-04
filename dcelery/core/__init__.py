from flask import Flask
from core import discovery
from core.extensions import db


def create_app(settings):
    app = Flask("dcelery")
    discovery.auto_discovery()
    # init sqlalchemy
    db.init_app(app)
    return app
