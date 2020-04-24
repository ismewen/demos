from celery.apps.beat import Beat

from core import create_app


class FlaskBeat(Beat):

    def run(self):
        import settings
        app = create_app(settings)
        with app.app_context():
            return super(FlaskBeat, self).run()
