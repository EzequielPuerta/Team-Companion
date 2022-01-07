import os
from team_companion.app.system.generic_system import GenericSystem
from team_companion.app.logging.setup import setup_logger
import logging

main_logger_name = "TEAM_COMPANION"

class LoggingSystem(GenericSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loggers = {}
        self.create_logger(main_logger_name, self.logging_path("main"))

    @classmethod
    def system_name(cls):
        return "logging_system"

    def logging_path(self, *args):
        return os.path.join(".", "logs", *args)

    def create_logger(self, name, path):
        setup_logger(name, path)
        self.loggers[name] = logging.getLogger(name)
        return self.loggers[name]

    def get_logger(self, logger_name):
        try:
            logger = self.loggers[logger_name]
        except KeyError:
            logger = self.loggers[main_logger_name]
        finally:
            return logger

    def start_logging(self, logger_name):
        self.create_logger(logger_name, self.logging_path(logger_name))

    def stop_logging(self, logger_name):
        del self.loggers[logger_name]

    ## Levels ##
    def debug(self, message, logger_name=main_logger_name):
        self.get_logger(logger_name).debug(message, stack_info=False, stacklevel=2)

    def info(self, message, logger_name=main_logger_name):
        self.get_logger(logger_name).info(message, stack_info=False, stacklevel=2)

    def warning(self, message, logger_name=main_logger_name):
        self.get_logger(logger_name).warning(message, stack_info=True, stacklevel=2)

    def error(self, message, logger_name=main_logger_name):
        self.get_logger(logger_name).error(message, stack_info=True, stacklevel=2)

    def critical(self, message, logger_name=main_logger_name):
        self.get_logger(logger_name).critical(message, stack_info=True, stacklevel=2)