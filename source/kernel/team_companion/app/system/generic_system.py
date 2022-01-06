from abc import ABC, abstractmethod
from team_companion.app.common.exceptions import UnexpectedError

class GenericSystem(ABC):
    def __init__(self, *args, **kwargs):
        self.root_system = kwargs.pop("root_system")
        super().__init__(*args, **kwargs)

    @classmethod
    def install_in(subsystem_class, root_system):
        subsystem = subsystem_class(root_system=root_system)
        root_system.register_by_message(subsystem_class.system_name(), subsystem)

    @classmethod
    @abstractmethod
    def system_name(self):
        pass

    def initialize(self):
        pass

    def should_not_implement(self):
        raise UserWarning("This method should not be implemented.")

    def unexpected_error(self, error_msg):
        raise UnexpectedError(f"Unexpected error: '{error_msg}'. The system could be inconsistent.")