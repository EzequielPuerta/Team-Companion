import time, pytz
from abc import ABC, abstractmethod
from datetime import datetime
from team_companion.conf.settings import current_timezone
from team_companion.app.system.generic_system import GenericSystem

class TimeSystem(GenericSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def system_name(cls):
        return "time_system"

    def sleep_for(self, seconds):
        time.sleep(seconds)

    def as_custom(self, format_string):
        return CustomFormatter(self, format_string)

    def as_user_friendly(self):
        return UserFriendlyFormatter(self)

    def as_timestamp(self):
        return TimestampFormatter(self)

    def now(self):
        return datetime.now()

    def utc_now(self):
        return datetime.utcnow()

    def tz_now(self):
        utc_timestamp = self.utc_now().replace(tzinfo=pytz.utc)
        return utc_timestamp.astimezone(pytz.timezone(current_timezone))

class TimeFormatter(ABC):
    def __init__(self, time_system, format_string):
        super().__init__()
        self.time_system = time_system
        self.format_string = format_string

    def formatting(self, time_value, on_failure=None):
        if time_value is None and on_failure is None:
            raise AssertionError("Error al obtener la fecha.")
        elif time_value is None and on_failure is not None:
            return on_failure()
        else:
            return time_value.strftime(self.format_string)

    def parsing(self, string_value, on_failure=None):
        if string_value is None and on_failure is None:
            raise AssertionError("Error al parsear la fecha.")
        elif string_value is None and on_failure is not None:
            return on_failure()
        else:
            return datetime.strptime(string_value, self.format_string)

    def now(self, on_failure=None):
        return self.formatting(self.time_system.now(), on_failure=on_failure)

    def utc_now(self, on_failure=None):
        return self.formatting(self.time_system.utc_now(), on_failure=on_failure)

    def tz_now(self, on_failure=None):
        return self.formatting(self.time_system.tz_now(), on_failure=on_failure)

class CustomFormatter(TimeFormatter):
    def __init__(self, time_system, format_string):
        super().__init__(time_system, format_string)

class UserFriendlyFormatter(TimeFormatter):
    def __init__(self, time_system):
        super().__init__(time_system, "%d/%m/%Y %H:%M:%S")

class TimestampFormatter(TimeFormatter):
    def __init__(self, time_system):
        super().__init__(time_system, "%d%m%Y%H%M%S")