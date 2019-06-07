#!/usr/bin/python3

import sys
import logging
import os
import time
import json
import binascii
from lib import *

'''
Tests error handling for wrong given get parameter.
'''

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    parse_config()

    device_name = __file__

    # Wrong mode.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last_wrong" \
               + "&device=" \
               + device_name
    logging.debug("[%s] Getting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Missing device for mode "last".
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last"
    logging.debug("[%s] Getting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Missing device for mode "view".
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=view" \
               + "&start=1" \
               + "&end=2"
    logging.debug("[%s] Getting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Missing start for mode "view".
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=view" \
               + "&device=" \
               + device_name \
               + "&end=2"
    logging.debug("[%s] Getting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Missing end for mode "view".
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=view" \
               + "&device=" \
               + device_name \
               + "&start=1"
    logging.debug("[%s] Getting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)