import os
import logging
from team_companion.app.logging.handler import TimedRotatingPathHandler, SpecificLoggingLevelFilter

def setup_logger(logger_name, root_path):
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    # File names
    info_log_file_name = os.path.join(root_path, 'info.log')
    error_log_file_name = os.path.join(root_path, 'errors.log')
    all_log_file_name = os.path.join(root_path, 'all.log')

    # Handlers
    info_file_handler = TimedRotatingPathHandler(info_log_file_name, root_path=root_path, when="midnight", interval=1, encoding='utf-8')
    errors_file_handler = TimedRotatingPathHandler(error_log_file_name, root_path=root_path, when="midnight", interval=1, encoding='utf-8')
    all_file_handler = TimedRotatingPathHandler(all_log_file_name, root_path=root_path, when="midnight", interval=1, encoding='utf-8')
    stream_handler = logging.StreamHandler()

    info_file_handler.suffix = "%Y-%m-%d"
    errors_file_handler.suffix = "%Y-%m-%d"
    all_file_handler.suffix = "%Y-%m-%d"

    # Formatters
    simple_formatter = logging.Formatter(fmt=u'%(asctime)s.%(msecs)03d | %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    full_formatter = logging.Formatter(fmt=u'%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s | (%(filename)s:%(lineno)s)', datefmt='%d/%m/%Y %H:%M:%S')

    info_file_handler.setFormatter(simple_formatter)
    errors_file_handler.setFormatter(full_formatter)
    all_file_handler.setFormatter(full_formatter)
    stream_handler.setFormatter(simple_formatter)

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.addFilter(SpecificLoggingLevelFilter(logging.INFO))
    errors_file_handler.setLevel(logging.WARNING)
    all_file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)

    # Logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(info_file_handler)
    logger.addHandler(errors_file_handler)
    logger.addHandler(all_file_handler)
    logger.addHandler(stream_handler)