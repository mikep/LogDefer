import json
import os
import re
import tempfile
import time

__version__ = "0.1.0"


class LogDefer(object):
    """
        Generate log object conpatible with log-defer-viz
        https://github.com/hoytech/Log-Defer-Viz
    """
    def __init__(self, options={}):
        self.levels = (40, 30, 20, 10)

        self.message = {
            'start': time.time(),
            'logs': [],
            'timers': {},
            'data': {},
        }

        if 'disable_incremental_logging' in options:
            self.tempfile = None
        else:
            if 'temp_file_path' in options:
                temp_file_path = options.get('temp_file_path')
            else:
                temp_file_path = "/tmp/log_defer_incremental_logs/"

            self.tempfile = tempfile.NamedTemporaryFile(
                dir=temp_file_path, delete=False, prefix=str(time.time()) + "."
            )


    def record_incremental_log(self):
        if self.tempfile:
            self.tempfile.write(
                str(self.__log_message_json__({time.time(): self.message})).encode('utf-8')
            )

    def add_message(self, level='30', message="", data=None, *args):
        """ Add message to log object """
        log = [self._get_et(), level, message]

        if data:
            if args:
                for arg in args:
                    data = dict(list(data.items()) + list(arg.items()))

            log.append(data)

        self.message['logs'].append(log)
        self.record_incremental_log()

    def timer(self, name=None):
        """
            Add timer to log object, If timer already
            exists, set the end time.
        """
        self.name = name
        if name and name not in self.message['timers']:
            self.message['timers'][name] = {
                'start': self._get_et(),
                'name': name,
            }
        else:
            self.message['timers'][name]['end'] = self._get_et()

        self.record_incremental_log()
        return self

    def __enter__(self):
        self.timer(self.name)

    def __exit__(self, a, b, c):
        self.timer(self.name)

    def data(self, d=None):
        """ Add data to log object """
        if d:
            self.message['data'] = dict(
                list(self.message['data'].items()) + list(d.items())
            )
        self.record_incremental_log()

    def finalize_log(self):
        """ Format and return the log object for logging. """
        self.__format_log_message_output__()
        formatted_log = self.__log_message_json__()

        if self.tempfile:
            os.remove(self.tempfile.name)

        return formatted_log

    def __format_log_message_output__(self):
        # Clean up, log-defer-viz doesn't like empty objects.
        for key in ('logs', 'timers', 'data'):
            if self.message[key] == [] or self.message[key] == {}:
                del self.message[key]

        # Convert timer to list.
        if 'timers' in self.message:
            timers = []
            for timer in self.message['timers']:
                timers.append([
                    self.message['timers'][timer]['name'],
                    self.message['timers'][timer]['start'],
                    self.message['timers'][timer].get('end', self._get_et())
                ])

            self.message['timers'] = timers

        # Record end time.
        self.message['end'] = self._get_et()

    def __log_message_json__(self, message=None):
        message = self.message if not message else message
        try:
            return json.dumps(message)
        except:
            def serialize_fix(m):
                try:
                    for i, x in enumerate(m):
                        try:
                            if type(m) == dict:
                                json.dumps(m[x])
                            else:
                                json.dumps(x)
                        except:
                            if type(m) == dict:
                                m[x] = serialize_fix(m[x])
                            elif type(m) == list:
                                m[i] = serialize_fix(x)
                            else:
                                m[x] = str(x)
                    return m
                except:
                    return str(m)

            return json.dumps(serialize_fix(message))

    # Log level functions
    def error(self, message='', data=None, *args):
        self.add_message(10, message, data, *args)

    def warn(self, message='', data=None, *args):
        self.add_message(20, message, data, *args)

    def info(self, message='', data=None, *args):
        self.add_message(30, message, data, *args)

    def debug(self, message='', data=None, *args):
        self.add_message(40, message, data, *args)

    # Util functions
    def _get_et(self):
        """
            log-defer-viz uses time since the start time in logs and timers
        """
        return time.time() - self.message['start']
