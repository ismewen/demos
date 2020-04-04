
from celery import Celery
from flask import current_app

import settings
from core import create_app


def make_celery(app):
    celery = Celery(
        app.import_name,
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = current_app if current_app else create_app(settings)

celery_app = make_celery(app=app)

