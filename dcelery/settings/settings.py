import arrow
from celery.schedules import crontab
from modules.routines.clockedschedule import clocked

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:ismewen@localhost:5432/dcelery"
BROKER_URL = 'amqp://ismewen:ismewen@localhost:5672//'
USE_TZ = False
TIME_ZONE = "UTC"
CELERYBEAT_SCHEDULE = {
    "say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": crontab(minute="*/1", hour=arrow.utcnow().hour)
    },
    "interval_say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": 3*10,
    },
    "clocked_say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": clocked(clocked_time=arrow.utcnow().shift(minutes=3).datetime, enabled=True),
    }
}
