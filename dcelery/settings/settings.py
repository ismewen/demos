from celery.schedules import crontab

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:ismewen@localhost:5432/dcelery"
BROKER_URL = 'amqp://ismewen:ismewen@localhost:5672//'
USE_TZ = False
TIME_ZONE ="UTC"
CELERYBEAT_SCHEDULE = {
    "say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": crontab(minute="*/1")
    },
    "interval_say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": 3,
    }
}
