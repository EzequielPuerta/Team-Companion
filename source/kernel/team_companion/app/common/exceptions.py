# INFO
class AppInfo(Exception):
    pass

# WARNING
class AppWarning(Exception):
    pass

class CouldNotBeLocked(AppWarning):
    pass

# ERROR
class AppError(Exception):
    pass

class UnexpectedError(AppError):
    pass