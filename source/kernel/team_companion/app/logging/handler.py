import logging, os, time, re
from logging.handlers import TimedRotatingFileHandler
from stat import ST_MTIME

class SpecificLoggingLevelFilter(object):
    def __init__(self, level):
        self.level = level

    def filter(self, logRecord):
        return logRecord.levelno == self.level

# Specialization of the logging.handlers.TimedRotatingFileHandler to
# rotate the logs by time not only in files, but also in folders
# https://github.com/python/cpython/blob/master/Lib/logging/handlers.py
class TimedRotatingPathHandler(TimedRotatingFileHandler):
    def __init__(self, filename, **kwargs) -> None:
        self.root_path = kwargs.pop('root_path', os.path.join('.'))
        super().__init__(filename, **kwargs)

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)

        sufixTime = time.strftime(self.suffix, timeTuple)
        fullPath = os.path.join(self.root_path, sufixTime)
        if not os.path.exists(fullPath):
            os.makedirs(fullPath)
        dfn = self.rotation_filename(os.path.join(fullPath, sufixTime + "." + os.path.basename(self.baseFilename)))

        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval

        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600
                else:
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt