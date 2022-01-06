from flask import Flask
from functools import partial
from team_companion.conf.settings import host, port

class RootSystem(Flask):
    def __init__(self, import_name, *args, **kwargs):
        super(RootSystem, self).__init__(import_name, *args, **kwargs)
        self.subsystems_by_message = {}
        self.subsystem_classes_to_install = []

    ## Configuration ##
    def installing(self, subsystem_classes):
        self.subsystem_classes_to_install = subsystem_classes

    ## Run ##
    def run(self, main_stop):
        self.main_stop = main_stop
        self.initialize()
        self.start_up()
        super(RootSystem, self).run(host=host, port=port)

    def initialize(self):
        [subsystem_class.install_in(self) for subsystem_class in self.subsystem_classes_to_install]
        for subsystem in self.subsystems_by_message.values():
            subsystem.initialize()
        self.subscribe_to_signals_of_interest()

    def start_up(self):
        with self.app_context():
            # to do after system initialization
            pass

    ## Subsystems ##
    def __getattr__(self, name: str):
        try:
            value = self.subsystems_by_message[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        else:
            return value

    def register_by_message(self, message_name, subsystem):
        self.subsystems_by_message[message_name] = subsystem

    ## Signaling ##
    def subscribe_to_signals_of_interest(self):
        pass # self.signal_system.subscribe(a_request, self.start_up_and_connect_callback)

    def start_up_and_connect_callback(self, current_sender, **kwargs):
        kwargs.pop("request").execute_in(self)