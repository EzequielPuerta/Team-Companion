import json
from blinker.base import ANY
from abc import ABC, abstractmethod

# Abstract request definition, all request definitions must inherit from this
class RequestDefinition(ABC):
    def __init__(self, **kwargs):
        self.sender = kwargs.get("sender", None)
        self.target = kwargs.get("target", None)
        self.on_success = kwargs.get("on_success", lambda : None)
        self.on_failure = kwargs.get("on_failure", lambda error_msg : None)
        self.handling = kwargs.get("handling", (Exception, ))
        if issubclass(type(self.handling), Exception):
            self.handling = (self.handling, )
        super().__init__()

    def signal_name(self):
        return self.__class__.__name__

    def routing_key(self):
        if not(self.sender is None) and self.target is None:
            routing_key = str(self.sender)
        elif self.sender is None and not(self.target is None):
            routing_key = str(self.target)
        elif not(self.sender is None) and not(self.target is None):
            routing_key = f"{self.sender}-{self.target}"
        else:
            routing_key = ANY
        return routing_key

    @abstractmethod
    def execute(self, root_system):
        pass

    def execute_in(self, root_system):
        with root_system.app_context():
            try:
                self.execute(root_system)
            except self.handling as error_msg:
                root_system.logging_system.error(error_msg)
                self.on_failure(error_msg)
            else:
                self.on_success()