## NAME

LogDefer - Deferred logs and timers

--

## Description

This module allows you to defer the writing of log messages until a "transaction" has completed. This transaction could be a HTTP Request or a cron job run.

This module doesn't actually write the logs, it just generates a structured log message. To write these messages to a log file use a [standard logging library](http://docs.python.org/2/library/logging.html)

--

## USAGE

### DATA

    from LogDefer import LogDefer

    log = LogDefer()
    log.data(dict(username="JoeUser", ipAddress="127.0.0.1")

    print log.finalize_log()

returns:

    {
        "start": 1387235881.810899, 
        "end": 2.5987625122070312e-05, 
        "data": {
            "username": "JoeUser", 
            "ipAddress": "127.0.0.1"
        }
    }

### TIMER

    from LogDefer import LogDefer

    log = LogDefer()
    with log.timer('timerName'):
        # Do something that takes a while
        someFunctionThatIsSlow()

    print log.finalize_log()

    # Note, Currently you cannot have two timers running concurrently

returns:

    {
        "start": 1387235881.811141, 
        "end": 0.5606820583343506, 
        "timers": [
            [
                "timerName", 
                9.059906005859375e-06, 
                0.5606479644775391
            ]
        ]
    }
 
### LOG LINES

Default Log Levels:
+ log.error('message') # 10
+ log.warn('message') # 20
+ log.info('message') # 30
+ log.debug('message') # 40

--

    log = LogDefer()

    log.error('error message')
    log.warn('warning message')
    log.info('info message')
    log.debug('debug message')

    print log.finalize_log()

returns:

    {
        "start": 1387235882.372069, 
        "end": 0.00010514259338378906, 
        "logs": [
            [
                1.0013580322265625e-05, 
                10, 
                "error message"
            ], 
            [
                1.811981201171875e-05, 
                20, 
                "warning message"
            ], 
            [
                2.3126602172851562e-05, 
                30, 
                "info message"
            ], 
            [
                2.8133392333984375e-05, 
                40, 
                "debug message"
            ]
        ]
    }

--

    # Log message with data and custom log level
    log = LogDefer()

    log.add_message(level=25, message='custom message', data=uuid.uuid4())

    print log.finalize_log()

returns:

    {
        "start": 1387236489.660819,
        "end": 0.00011897087097167969,
        "logs": [
            [
                0.00010895729064941406,
                25,
                "custom message", 
                {
                    "log_specific_data": "d37eb4fc-1c0c-41fa-beb0-9f96c9b9836e"
                }
            ]
        ]
    }


## INSTALLATION

    $ pip install LogDefer


## SEE ALSO

+ Perl Implimentation: [Log::Defer github repo](https://github.com/hoytech/Log-Defer)
+ Log Viewer: [log-defer-viz github repo](https://github.com/hoytech/Log-Defer-Viz)



## AUTHOR

Michael Pucyk <michael.pucyk@gmail.com>


