from team_companion.app.system.generic_system import GenericSystem
from blinker import signal

class SignalSystem(GenericSystem):
    def __init__(self, *args, **kwargs):
        self._available_signals = {}
        super().__init__(*args, **kwargs)

    @classmethod
    def system_name(cls):
        return "signal_system"

    def _add(self, signal_name):
        _signal = signal(signal_name)
        self._available_signals[signal_name] = _signal
        return _signal

    def _select(self, signal_name):
        try:
            _signal = self._available_signals[signal_name]
        except KeyError:
            _signal = self._add(signal_name)
        finally:
            return _signal

    def publish(self, request):
        kwargs = {"request":request}
        self._select(request.signal_name()).send(request.routing_key(), **kwargs)

    def subscribe(self, request, callback):
        self._select(request.signal_name()).connect(callback, sender=request.routing_key())