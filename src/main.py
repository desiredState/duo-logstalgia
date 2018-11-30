#!/usr/bin/env python3

""" duo-logstalgia
Streams Duo Authentication Logs to Logstalgia Custom Log Format.
See README.md for documentation.
"""

import logging
import os
import pprint
import sys
import time

import duo_client

from lib.logger import Logger

# Initialise a global logger.
try:
    logger = logging.getLogger('duo_logstalgia')
    logger.setLevel(logging.INFO)

    # We're in Docker, so just log to stdout.
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    out.setFormatter(formatter)
    logger.addHandler(out)

except Exception as e:
    print("Failed to initialise logging with exception:\n{}".format(e))
    sys.exit(1)


class DuoLogstalgia(object):
    """ Streams Duo Authentication Logs to Logstalgia Custom Log Format. """

    def __init__(self):
        """ """

        self.logger = Logger()
        self.pp = pprint.PrettyPrinter(indent=4)

        # Get Duo API key environment variables.
        try:
            ikey = os.environ['DUO_IKEY']
            skey = os.environ['DUO_SKEY']
            host = os.environ['DUO_HOST']

        except KeyError:
            self.logger("Missing config environment variable "
                        "(required: DUO_IKEY, DUO_SKEY and DUO_HOST).",
                        'exception')
            sys.exit(1)

        # Create a Duo Admin API client.
        try:
            self.admin_api = duo_client.Admin(
                ikey=ikey,
                skey=skey,
                host=host
            )

        except Exception as e:
            self.logger("Failed to connect to Duo Admin API with error:"
                        "\n{}".format(e), 'exception')
            sys.exit(1)

    def __call__(self):
        """ """

        interval = 15  # How often to pull logs in seconds.
        mintime = time.time() - interval

        while True:
            try:
                auth_log = self.admin_api.get_authentication_log(
                    mintime=mintime
                )

                for line in auth_log:
                    formatted_line = self.format_as_logstalgia(line)
                    print(formatted_line)

            # Fail silently and re-try next time as to not confuse Logstalgia.
            except Exception as e:
                print(e)

            time.sleep(interval)

    def format_as_logstalgia(self, line):
        """
        Convert a Duo Auth Log line to Logstalgia Custom Log Format.
        :param line: (dict) The raw Duo Auth Log line.
        :return formatted_line: (str) The formatted log line.
        """

        if line['result'] == "SUCCESS":
            response_code = '200'
            success = "1"
            # response_colour = "#008000"
        else:
            response_code = '500'
            success = "0"
            # response_colour = "#FF0000"

        timestamp = line['timestamp']
        hostname = line['ip']
        path = line['integration']
        response_size = "1000"
        # referrer_url =
        # user_agent =
        # virtual_host =
        # pid_other =

        formatted_line = "{}|{}|{}|{}|{}|{}".format(
            timestamp,
            hostname,
            path,
            response_code,
            response_size,
            success,
            # response_colour,
            # referrer_url,
            # user_agent,
            # virtual_host,
            # pid_other
        )

        return formatted_line


if __name__ == "__main__":
    daemon = DuoLogstalgia()
    daemon()
