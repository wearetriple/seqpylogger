"""
Module: containing helper functions
"""
import threading
import functools


def set_interval(interval):
    """Decorator function to add SetInterval

    Parameters
    ----------
    interval : int
        Seconds when every repeat should happen
    """

    def decorator_threaded_timer(func):
        @functools.wraps(func)
        def wrapper_threaded_timer(*args, **kwargs):
            SetInterval(func, interval, args=args, kwargs=kwargs)

        return wrapper_threaded_timer

    return decorator_threaded_timer


def url_add_trailing_slash(uri: str) -> str:
    """Add trailing slash to url if this is valid

    Parameters
    ----------
    uri : str
        Web address to update

    Returns
    -------
    str
        uri or updated uri
    """

    if len(uri) == 0 or uri[-1] == "/":
        return uri

    split_uri = str.split(uri, "/")

    if len(split_uri) == 0:
        return f"{uri}/"
    if len(split_uri[-1]) > 1 and "?" not in split_uri[-1]:
        return f"{uri}/"
    return uri


class SetInterval:
    """SetInterval class inspired bij js setInterval(function, interval)
    Also has args, kwargs functionality
    """

    def __init__(self, function, seconds, *args, **kwargs):
        self.interval_seconds = seconds
        self.repeating_function = function
        self._args = args
        self._kwargs = kwargs
        self._set_next_time()

    def _interval_handler(self, args, kwargs):
        self.repeating_function(*args, **kwargs)
        self._set_next_time()

    def _set_next_time(self):
        thread = threading.Timer(
            interval=self.interval_seconds,
            function=self._interval_handler,
            args=self._args,
            kwargs=self._kwargs,
        )
        thread.daemon = True
        thread.start()
