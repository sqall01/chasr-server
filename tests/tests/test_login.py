#!/usr/bin/python3

import sys
import requests
import logging
import os
from lib import *

'''
Tests a successful login attempt.
'''

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    parse_config()

    device_name = __file__
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last&device=" + device_name
    request_result = send_post_request(location, payload, file_name)

    if request_result["code"] == ErrorCodes.NO_ERROR:
        sys.exit(0)
    else:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, r.text))
        sys.exit(1)