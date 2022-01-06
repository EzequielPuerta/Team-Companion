from team_companion.app.system.generic_system import GenericSystem
from threading import Lock
import json

class ToastrSystem(GenericSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutex = Lock()
        self.notifications = []

    @classmethod
    def system_name(cls):
        return "toastr_system"

    def notify(self, message, category, title=None):
        jsonData = {}
        jsonData["category"] = category
        jsonData["message"] = message
        jsonData["title"] = title
        self.mutex.acquire()
        self.notifications.append(json.dumps(jsonData, ensure_ascii=False))
        self.mutex.release()

    def notify_info(self, message, title=None):
        self.notify(message, "info", title=title)

    def notify_success(self, message, title=None):
        self.notify(message, "success", title=title)

    def notify_warning(self, message, title=None):
        self.notify(message, "warning", title=title)

    def notify_error(self, message, title=None):
        self.notify(message, "error", title=title)

    def consume(self):
        while True:
            self.mutex.acquire()
            if len(self.notifications) > 0:
                new_event = f"data: {self.notifications.pop(0)}\n\n"
                self.mutex.release()
                yield new_event
            else:
                self.mutex.release()
            self.root_system.time_system.sleep_for(1)