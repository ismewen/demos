import pytz

from sqlalchemy import String


def is_pytz_instance(value):
    return value is pytz.UTC or isinstance(value, pytz.tzinfo.BaseTzInfo)



class TzString(String):

    def bind_processor(self, dialect):
        return str

    def result_processor(self, dialect, coltype):
        "Returns a tuple of (python representation, db representation)"
        def process(value):
            if value is None or value == '':
                return None
            if is_pytz_instance(value):
                return value
            try:
                return pytz.timezone(str(value))
            except pytz.UnknownTimeZoneError:
                pass
        return process


