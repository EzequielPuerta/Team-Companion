import time
import signal
import sys
import threading
from team_companion.app import create_app

root_system = create_app()

# Auxs
def signal_handler_over(sig, frame, core_app):
    global stop_threads
    stop_threads = True
    core_app.join()
    sys.exit(0)

# Main Thread
if __name__=='__main__':
    stop_threads = False

    root_system.run(lambda : stop_threads)

    # Handler of Ctrl+C Event
    signal.signal(signal.SIGINT, lambda signal, frame: signal_handler_over(signal, frame, threading.main_thread()))

    while True:
        time.sleep(1)