from team_companion.app.system.generic_system import GenericSystem
from team_companion.app.web.modules.log_time.models import LogTime
import requests
import datetime

class LogTimeSystem(GenericSystem):

    @classmethod
    def system_name(cls):
        return "log_time_system"

    def select_all(self):
        now = self.root_system.time_system.tz_now() - datetime.timedelta(days=31)
        period = f"{now.year}-{now.month}"
        all_log_times = []
        for internal_user in self.root_system.internal_user_system.select_all():
            raw_url = f"http://srvintranet.mercap.net:9000/worklog/user/{internal_user.username}?period={period}"
            response = requests.get(raw_url)
            if response.status_code == 404:
                self.root_system.toastr_system.notify_warning(response.text, title=internal_user.username)
            elif response.status_code == 500:
                self.root_system.toastr_system.notify_warning(response.text, title=period)
            else:
                all_log_times.append(LogTime(response.json()))
        return all_log_times