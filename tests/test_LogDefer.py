import json
import unittest
import time

from LogDefer import LogDefer

log_levels = {
    40: 'debug',
    30: 'info',
    20: 'warn',
    10: 'error'
}


class LogDeferTest(unittest.TestCase):
    def setUp(self):
        self.logger = LogDefer()

    def test_default_levels(self):
        self.assertEqual(self.logger.levels, (40, 30, 20, 10))

    def test_message_object(self):
        self.assertTrue('start' in self.logger.message)
        self.assertTrue('logs' in self.logger.message)
        self.assertTrue('timers' in self.logger.message)
        self.assertTrue('data' in self.logger.message)

        self.assertTrue(
            type(self.logger.message['start']),
            float
        )

        self.assertTrue(
            type(self.logger.message['logs']),
            list
        )

        self.assertTrue(
            type(self.logger.message['timers']),
            dict
        )

        self.assertTrue(
            type(self.logger.message['data']),
            dict
        )

    def test_empty_log_defer_object(self):
        # Log defer message should only have start and end if no
        # logs/timers/data is added.
        #
        log_object = self.__log_defer_to_dict__()

        self.assertEqual(len(list(log_object.keys())), 2)

        self.assertTrue('start' in log_object)
        self.assertTrue('end' in log_object)

        self.assertFalse('logs' in log_object)
        self.assertFalse('timers' in log_object)
        self.assertFalse('data' in log_object)

    def test_log_one_message(self):
        # Logging one message should only have 1 log object in the output
        # message.
        #

        log_message = "This is a debug message"
        self.logger.debug(log_message)
        log_object = self.__log_defer_to_dict__()

        self.assertTrue('logs' in log_object)

        self.assertEqual(type(log_object['logs']), list)
        self.assertEqual(len(log_object['logs']), 1)

        self.assertEqual(type(log_object['logs'][0]), list)
        self.assertEqual(len(log_object['logs'][0]), 3)

        # LogDefer log message format:
        # [elapsedTime, logLevel, logMessage, <data>]
        #
        message = log_object['logs'][0]

        # elapsedTime
        self.assertEqual(type(message[0]), float)
        self.assertTrue(message[0] < log_object['end'])

        # logLevel
        self.assertEqual(type(message[1]), int)
        self.assertEqual(log_levels[message[1]], 'debug')

        # logMessage
        self.assertEqual(message[2], log_message)

    def test_log_one_message_with_data(self):
        # Logging one message should only have 1 log object in the output
        # message and it should have a data object.
        #

        log_message = "This is a debug message"
        log_data = {"key": "value", "123": "abc"}

        self.logger.debug(log_message, log_data)
        log_object = self.__log_defer_to_dict__()

        self.assertTrue('logs' in log_object)

        self.assertEqual(type(log_object['logs']), list)
        self.assertEqual(len(log_object['logs']), 1)

        self.assertEqual(type(log_object['logs'][0]), list)
        self.assertEqual(len(log_object['logs'][0]), 4)

        # LogDefer log message format:
        # [elapsedTime, logLevel, logMessage, <data>]
        #
        message = log_object['logs'][0]

        # elapsedTime
        self.assertEqual(type(message[0]), float)
        self.assertTrue(message[0] < log_object['end'])

        # logLevel
        self.assertEqual(type(message[1]), int)
        self.assertEqual(log_levels[message[1]], 'debug')

        # logMessage
        self.assertEqual(message[2], log_message)

        # data
        self.assertEqual(type(message[3]), dict)
        self.assertTrue("key" in message[3])
        self.assertTrue("123" in message[3])

        for k in list(log_data.keys()):
            self.assertEqual(message[3][k], log_data[k])

    def test_log_multiple_messages(self):
        # Logging one message should only have 1 log object in the output
        # message and it should have a data object.
        #

        log_messages = [
            "debug",
            "info",
            "warn",
            "error",
            "warn"
        ]

        log_data = [
            None,
            None,
            {"key": "value", "123": "abc"},
            None,
            {"key": "value", "123": "abc"},
        ]

        self.logger.debug(log_messages[0], log_data[0])
        self.logger.info(log_messages[1], log_data[1])
        self.logger.warn(log_messages[2], log_data[2])
        self.logger.error(log_messages[3], log_data[3])
        self.logger.add_message(20, log_messages[4], log_data[4])

        log_object = self.__log_defer_to_dict__()

        self.assertTrue('logs' in log_object)

        self.assertEqual(type(log_object['logs']), list)
        self.assertEqual(len(log_object['logs']), 5)

        for i, log in enumerate(log_object['logs']):
            self.assertEqual(type(log), list)
            if log_data[i]:
                self.assertEqual(len(log), 4)
            else:
                self.assertEqual(len(log), 3)

            # LogDefer log message format:
            # [elapsedTime, logLevel, logMessage, <data>]
            #

            # elapsedTime
            self.assertEqual(type(log[0]), float)
            self.assertTrue(log[0] < log_object['end'])

            # logLevel
            self.assertEqual(type(log[1]), int)
            self.assertEqual(log_levels[log[1]], log_messages[i])

            # logMessage
            self.assertEqual(log[2], log_messages[i])

            if log_data[i]:
                # data
                self.assertEqual(type(log[3]), dict)

                for k in list(log_data[i].keys()):
                    self.assertEqual(log[3][k], log_data[i][k])

    def test_log_timer(self):
        with self.logger.timer("junktimer"):
            time.sleep(0.01)

        log_object = self.__log_defer_to_dict__()
        self.assertTrue('timers' in log_object)

        self.assertEqual(log_object['timers'][0][0], 'junktimer')
        self.assertEqual(len(log_object['timers']), 1)

        self.assertEqual("{timer:.2f}".format(
            timer=(log_object['timers'][0][2] - log_object['timers'][0][1])), '0.01'
        )

    def test_log_timers(self):
        with self.logger.timer("junktimer"):
            time.sleep(0.01)

        with self.logger.timer("junktimer2"):
            time.sleep(0.01)

        log_object = self.__log_defer_to_dict__()
        self.assertTrue('timers' in log_object)

        self.assertEqual(log_object['timers'][0][0], 'junktimer')
        self.assertEqual(log_object['timers'][1][0], 'junktimer2')
        self.assertEqual(len(log_object['timers']), 2)

        self.assertEqual("{timer:.2f}".format(
            timer=(log_object['timers'][0][2] - log_object['timers'][0][1])), '0.01'
        )

        self.assertEqual("{timer:.2f}".format(
            timer=(log_object['timers'][1][2] - log_object['timers'][1][1])), '0.01'
        )

    def test_data(self):
        data = {'key': 'value'}
        self.logger.data(data)

        log_object = self.__log_defer_to_dict__()
        self.assertTrue('data' in log_object)
        self.assertEqual(data, log_object['data'])

    def test_message_data(self):
        data = {'key': 'value'}
        more = {'k2': 'v2'}
        self.logger.warn("aaa", data, more)

        log_object = self.__log_defer_to_dict__()
        self.assertTrue('logs' in log_object)
        self.assertEqual(
            dict(list(data.items()) + list(more.items())), log_object['logs'][0][-1]
        )

    def test_data_non_serializable_object(self):
        data = {'key': self.logger}

        self.logger.data(data)
        self.logger.data({'key2': [self.logger, self.logger]})

        self.logger.debug('message', [self.logger, self.logger])
        self.logger.debug('message', (self.logger, self.logger))

        self.logger.warn('junk', self.logger)

        log_object = self.__log_defer_to_dict__()
        self.assertTrue('data' in log_object)

        self.assertEqual(2, len(list(log_object['data'].keys())))
        self.assertEqual(log_object['data']['key'], str(data['key']))

    def __log_defer_to_dict__(self):
        json_output = self.logger.finalize_log()
        return json.loads(json_output)


if __name__ == "__main__":
    unittest.main()
