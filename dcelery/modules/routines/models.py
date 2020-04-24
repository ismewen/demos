from datetime import timedelta

import arrow
from celery import schedules
from flask_babel import gettext as _
from sqlalchemy import func

from core import db
from modules.routines.sqltypes import TzString
from .tzcrontab import TzAwareCrontab
from .utils import make_aware, now
from .clockedschedule import clocked

import settings

DAYS = 'days'
HOURS = 'hours'
MINUTES = 'minutes'
SECONDS = 'seconds'
MICROSECONDS = 'microseconds'

PERIOD_CHOICES = (
    (DAYS, _('Days')),
    (HOURS, _('Hours')),
    (MINUTES, _('Minutes')),
    (SECONDS, _('Seconds')),
    (MICROSECONDS, _('Microseconds')),
)

SINGULAR_PERIODS = (
    (DAYS, _('Day')),
    (HOURS, _('Hour')),
    (MINUTES, _('Minute')),
    (SECONDS, _('Second')),
    (MICROSECONDS, _('Microsecond')),
)

SOLAR_SCHEDULES = [(x, _(x)) for x in sorted(schedules.solar._all_events)]


def cronexp(field):
    """Representation of cron expression."""
    return field and str(field).replace(' ', '') or '*'


class ScheduleBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128))

    __mapper_args__ = {
        'polymorphic_identity': 'Schedule',
        'polymorphic_on': type
    }

    def save(self):
        db.session.add(self)
        db.session.commit()


class SolarSchedule(ScheduleBase):
    """Schedule following astronomical patterns.

    Example: to run every sunrise in New York City:
    event='sunrise', latitude=40.7128, longitude=74.0060
    """

    id = db.Column(db.Integer, db.ForeignKey(ScheduleBase.id), primary_key=True)
    event = db.Column(db.String(24), doc=_("Solar Event"))
    latitude = db.Column(db.Numeric(9, 6), doc=_("Latitude"))
    longitude = db.Column(db.Numeric(9, 6), doc=_("Longtitude"))

    __mapper_args__ = {
        'polymorphic_identity': 'SolarSchedule',
    }

    @property
    def schedule(self):
        return schedules.solar(self.event,
                               self.latitude,
                               self.longitude,
                               nowfun=lambda: arrow.utcnow().datetime)

    @classmethod
    def from_schedule(cls, schedule):
        spec = {'event': schedule.event,
                'latitude': schedule.lat,
                'longitude': schedule.lon}
        return cls(**spec)

    def __str__(self):
        return '{0} ({1}, {2})'.format(
            self.get_event_display(),
            self.latitude,
            self.longitude
        )


class IntervalSchedule(ScheduleBase):
    """Schedule executing on a regular interval.

    Example: execute every 2 days
    every=2, period=DAYS
    """

    DAYS = DAYS
    HOURS = HOURS
    MINUTES = MINUTES
    SECONDS = SECONDS
    MICROSECONDS = MICROSECONDS

    PERIOD_CHOICES = PERIOD_CHOICES

    period = db.Column(db.String(24))
    every = db.Column(db.Integer)
    id = db.Column(db.Integer, db.ForeignKey(ScheduleBase.id), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'IntervalSchedule',
    }

    @property
    def schedule(self):
        return schedules.schedule(
            timedelta(**{self.period: self.every}),
            nowfun=lambda: make_aware(now())
        )

    @classmethod
    def from_schedule(cls, schedule, period=SECONDS):
        every = max(schedule.run_every.total_seconds(), 0)
        return cls(every=every, period=period)

    def __str__(self):
        readable_period = None
        if self.every == 1:
            for period, _readable_period in SINGULAR_PERIODS:
                if period == self.period:
                    readable_period = _readable_period.lower()
                    break
            return _('every {}').format(readable_period)
        for period, _readable_period in PERIOD_CHOICES:
            if period == self.period:
                readable_period = _readable_period.lower()
                break
        return _('every {} {}').format(self.every, readable_period)

    @property
    def period_singular(self):
        return self.period[:-1]


class ClockedSchedule(ScheduleBase):
    """clocked schedule."""
    id = db.Column(db.Integer, db.ForeignKey(ScheduleBase.id), primary_key=True)
    clocked_time = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'ClockedSchedule',
    }

    def __str__(self):
        return '{} {}'.format(self.clocked_time, self.enabled)

    @property
    def schedule(self):
        c = clocked(clocked_time=self.clocked_time,
                    enabled=self.enabled, model=self)
        return c

    @classmethod
    def from_schedule(cls, schedule):
        spec = {'clocked_time': schedule.clocked_time,
                'enabled': schedule.enabled}
        return cls(**spec)


class CrontabSchedule(ScheduleBase):
    """Timezone Aware Crontab-like schedule.

    Example:  Run every hour at 0 minutes for days of month 10-15
    minute="0", hour="*", day_of_week="*",
    day_of_month="10-15", month_of_year="*"
    """

    #
    # The worst case scenario for day of month is a list of all 31 day numbers
    # '[1, 2, ..., 31]' which has a length of 115. Likewise, minute can be
    # 0..59 and hour can be 0..23. Ensure we can accomodate these by allowing
    # 4 chars for each value (what we save on 0-9 accomodates the []).
    # We leave the other fields at their historical length.
    #
    id = db.Column(db.Integer, db.ForeignKey(ScheduleBase.id, ondelete=""), primary_key=True)
    minute = db.Column(db.String(60 * 4), default="*", doc=_("Minute(s)"))
    hour = db.Column(db.String(24 * 4), default="*", doc=_("Hour's"))
    day_of_week = db.Column(db.String(64), default="*")
    day_of_month = db.Column(db.String(64), default="*")
    month_of_year = db.Column(db.String(64), default="*")
    timezone = db.Column(TzString(32), default="*")

    __mapper_args__ = {
        'polymorphic_identity': 'CrontabSchedule',
    }

    def __str__(self):
        return '{0} {1} {2} {3} {4} (m/h/d/dM/MY) {5}'.format(
            cronexp(self.minute), cronexp(self.hour),
            cronexp(self.day_of_week), cronexp(self.day_of_month),
            cronexp(self.month_of_year), str(self.timezone)
        )

    @property
    def schedule(self):
        crontab = schedules.crontab(
            minute=self.minute,
            hour=self.hour,
            day_of_week=self.day_of_week,
            day_of_month=self.day_of_month,
            month_of_year=self.month_of_year,
        )
        if getattr(settings, 'DJANGO_CELERY_BEAT_TZ_AWARE', True):
            crontab = TzAwareCrontab(
                minute=self.minute,
                hour=self.hour,
                day_of_week=self.day_of_week,
                day_of_month=self.day_of_month,
                month_of_year=self.month_of_year,
                tz=self.timezone
            )
        return crontab

    @classmethod
    def from_schedule(cls, schedule):
        spec = {'minute': schedule._orig_minute,
                'hour': schedule._orig_hour,
                'day_of_week': schedule._orig_day_of_week,
                'day_of_month': schedule._orig_day_of_month,
                'month_of_year': schedule._orig_month_of_year,
                'timezone': str(schedule.tz)
                }
        return cls(**spec)


class PeriodicTasks(db.Model):
    """Helper table for tracking updates to periodic tasks.

    This stores a single row with ident=1.  last_update is updated
    via django signals whenever anything is changed in the PeriodicTask model.
    Basically this acts like a DB data audit trigger.
    Doing this so we also track deletions, and not just insert/update.
    """

    ident = db.Column(db.SmallInteger, primary_key=True, unique=True)
    last_update = db.Column(db.DateTime, nullable=True)

    @classmethod
    def changed(cls, instance, **kwargs):
        if not instance.no_changes:
            cls.update_changed()

    @classmethod
    def update_changed(cls, **kwargs):
        obj = cls.query.filter(cls.ident == 1).first()
        if obj:
            obj.last_update = arrow.utcnow().datetime
        else:
            obj = cls(ident=1, last_update=arrow.utcnow().datetime)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def last_change(cls):
        obj = cls.query.filter(cls.ident == 1).first()
        if obj:
            return obj.last_update


class PeriodicTask(db.Model):
    """Model representing a periodic task."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    task = db.Column(db.String(200))

    # TODO: Redo this as a GenericForeignKey
    args = db.Column(db.Text, default='[]')
    kwargs = db.Column(db.Text, default="{}", nullable=True)
    queue = db.Column(db.String(200), nullable=True, default=None)
    exchange = db.Column(db.String(200), nullable=True, default=None)
    routing_key = db.Column(db.String(200), nullable=True, default=None)
    headers = db.Column(db.Text, nullable=True, default=None)
    priority = db.Column(db.SmallInteger, nullable=True, default=None)
    expires = db.Column(db.DateTime, nullable=True, default=None)
    expire_seconds = db.Column(db.Integer, nullable=True, default=None)
    one_off = db.Column(db.Boolean, default=False)
    start_time = db.Column(db.DateTime, nullable=True)
    enabled = db.Column(db.Boolean, nullable=True, default=True)
    last_run_at = db.Column(db.DateTime, default=func.now())
    total_run_count = db.Column(db.Integer, default=0)
    date_changed = db.Column(db.DateTime, onupdate=func.now())
    description = db.Column(db.Text, nullable=True)

    schedule_id = db.Column(db.ForeignKey(ScheduleBase.id), nullable=True)
    model_schedule = db.relationship(ScheduleBase, uselist=False)

    no_changes = False

    def validate_unique(self, *args, **kwargs):
        # clocked must be one off task
        if isinstance(self.model_schedule, ClockedSchedule) and not self.model_schedule.one_off:
            err_msg = 'clocked must be one off, one_off must set True'
            raise Exception(err_msg)

    def save(self, *args, **kwargs):
        self.exchange = self.exchange or None
        self.routing_key = self.routing_key or None
        self.queue = self.queue or None
        self.headers = self.headers or None
        if not self.enabled:
            self.last_run_at = None
        self._clean_expires()
        self.validate_unique()
        db.session.add(self)
        db.session.commit()

    def _clean_expires(self):
        if self.expire_seconds is not None and self.expires:
            raise Exception(
                _('Only one can be set, in expires and expire_seconds')
            )

    @property
    def expires_(self):
        return self.expires or self.expire_seconds

    def __str__(self):
        fmt = '{0.name}: {{no schedule}}'
        if self.model_schedule:
            fmt = "{0.name}: {0.model_schedule}"
        return fmt.format(self)

    @property
    def schedule(self):
        return self.model_schedule.schedule

    def delete(self, using=None, keep_parents=False):
        delete_entry = self.interval or self.crontab or self.solar or self.clocked
        delete_entry.delete()
        return super(PeriodicTask, self).delete(using=using, keep_parents=keep_parents)


"""
[event_t(time=1587697359.352167, priority=5, entry=<ModelEntry: say_hello modules.routines.tasks.say_hello(*[], **{}) <crontab: */1 *
         * *
          * (m/h/d/dM/MY), UTC>
        >), event_t(time=1587726124.36578, priority=5, entry=<ModelEntry: interval_say_hello modules.routines.tasks.say_hello(*[], **{}) <freq: 3.00 seconds>>), 
        
        event_t(time=1587700814.284076, priority=5, entry=<ModelEntry: celery.backend_cleanup celery.backend_cleanup(*[], **{}) <crontab: 0 4
         * *
          * (m/h/d/dM/MY), UTC>
        >)]
"""
