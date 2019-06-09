#!/usr/bin/python3

import sys
import logging
import os
import time
import json
import binascii
from lib import *

'''
Tests error handling for wrong given submit parameter.
'''

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    parse_config()

    device_name = __file__
    utctime = int(time.time())

    # Delete device to make sure no data is left.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/delete.php?mode=device" \
               + "&device=" \
               + device_name
    logging.debug("[%s] Deleting gps device." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if (request_result["code"] == ErrorCodes.NO_ERROR
       or (request_result["code"] == ErrorCodes.ILLEGAL_MSG_ERROR
       and request_result["msg"] == "Device does not exist.")):
        pass
    else:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Check if server does not have any data left.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last" \
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
    if request_result["msg"] != "Device does not exist.":
        logging.error("[%s] Response contains wrong error message. "
                      % file_name
                      + "Deleting device failed.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Missing gps_data for submission.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/submit.php"
    logging.debug("[%s] Submitting gps data (missing gps_data)." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Get submitted data and check received data.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last" \
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
    if request_result["msg"] != "Device does not exist.":
        logging.error("[%s] Response contains wrong error message. "
                      % file_name
                      + "Server submitted data.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    data_32_keys = ["iv", "lat", "lon", "alt", "speed"]
    for curr_key in data_32_keys:

        # Missing key in gps_data.
        gps_data = dict()
        gps_data["utctime"] = utctime
        gps_data["device_name"] = device_name
        for key in data_32_keys:
            if key == curr_key:
                continue
            gps_data[key] = "A"*32
        payload = {"user": Settings.username,
                   "password": Settings.password,
                   "gps_data": json.dumps([gps_data])}
        location = "/submit.php"
        logging.debug("[%s] Submitting gps data (missing %s in gps_data)."
                      % (curr_key, file_name))
        request_result = send_post_request(location, payload, file_name)
        if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
            logging.error("[%s] Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        # Get submitted data and check received data.
        payload = {"user": Settings.username,
                   "password": Settings.password}
        location = "/get.php?mode=last" \
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
        if request_result["msg"] != "Device does not exist.":
            logging.error("[%s] Response contains wrong error message. "
                          % file_name
                          + "Server submitted data.")
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        # Short key in gps_data.
        gps_data = dict()
        gps_data["utctime"] = utctime
        gps_data["device_name"] = device_name
        for key in data_32_keys:
            if key == curr_key:
                gps_data[key] = "B"*31
            else:
                gps_data[key] = "A"*32
        payload = {"user": Settings.username,
                   "password": Settings.password,
                   "gps_data": json.dumps([gps_data])}
        location = "/submit.php"
        logging.debug("[%s] Submitting gps data (short %s in gps_data)."
                      % (curr_key, file_name))
        request_result = send_post_request(location, payload, file_name)
        if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
            logging.error("[%s] Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        # Get submitted data and check received data.
        payload = {"user": Settings.username,
                   "password": Settings.password}
        location = "/get.php?mode=last" \
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
        if request_result["msg"] != "Device does not exist.":
            logging.error("[%s] Response contains wrong error message. "
                          % file_name
                          + "Server submitted data.")
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        # Long key in gps_data.
        gps_data = dict()
        gps_data["utctime"] = utctime
        gps_data["device_name"] = device_name
        for key in data_32_keys:
            if key == curr_key:
                gps_data[key] = "B"*33
            else:
                gps_data[key] = "A"*32
        payload = {"user": Settings.username,
                   "password": Settings.password,
                   "gps_data": json.dumps([gps_data])}
        location = "/submit.php"
        logging.debug("[%s] Submitting gps data (long %s in gps_data)."
                      % (curr_key, file_name))
        request_result = send_post_request(location, payload, file_name)
        if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
            logging.error("[%s] Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        # Get submitted data and check received data.
        payload = {"user": Settings.username,
                   "password": Settings.password}
        location = "/get.php?mode=last" \
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
        if request_result["msg"] != "Device does not exist.":
            logging.error("[%s] Response contains wrong error message. "
                          % file_name
                          + "Server submitted data.")
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

    # Missing utctime in gps_data.
    gps_data = dict()
    gps_data["device_name"] = device_name
    for key in data_32_keys:
        gps_data[key] = "A"*32
    payload = {"user": Settings.username,
               "password": Settings.password,
               "gps_data": json.dumps([gps_data])}
    location = "/submit.php"
    logging.debug("[%s] Submitting gps data (missing utctime in gps_data)."
                  % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Get submitted data and check received data.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last" \
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
    if request_result["msg"] != "Device does not exist.":
        logging.error("[%s] Response contains wrong error message. "
                      % file_name
                      + "Server submitted data.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # utctime not integer in gps_data.
    gps_data = dict()
    gps_data["utctime"] = "ABCD"
    gps_data["device_name"] = device_name
    for key in data_32_keys:
        gps_data[key] = "A"*32
    payload = {"user": Settings.username,
               "password": Settings.password,
               "gps_data": json.dumps([gps_data])}
    location = "/submit.php"
    logging.debug("[%s] Submitting gps data (utctime not integer in gps_data)."
                  % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Get submitted data and check received data.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last" \
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
    if request_result["msg"] != "Device does not exist.":
        logging.error("[%s] Response contains wrong error message. "
                      % file_name
                      + "Server submitted data.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Missing device_name in gps_data.
    gps_data = dict()
    gps_data["utctime"] = utctime
    for key in data_32_keys:
        gps_data[key] = "A"*32
    payload = {"user": Settings.username,
               "password": Settings.password,
               "gps_data": json.dumps([gps_data])}
    location = "/submit.php"
    logging.debug("[%s] Submitting gps data (missing device_name in gps_data)."
                  % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Get submitted data and check received data.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last" \
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
    if request_result["msg"] != "Device does not exist.":
        logging.error("[%s] Response contains wrong error message. "
                      % file_name
                      + "Server submitted data.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Long device_name in gps_data.
    long_device_name = "A"*256
    gps_data = dict()
    gps_data["utctime"] = utctime
    gps_data["device_name"] = long_device_name
    for key in data_32_keys:
        gps_data[key] = "A"*32
    payload = {"user": Settings.username,
               "password": Settings.password,
               "gps_data": json.dumps([gps_data])}
    location = "/submit.php"
    logging.debug("[%s] Submitting gps data (long device_name in gps_data)."
                  % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Get submitted data and check received data.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last" \
               + "&device=" \
               + long_device_name
    logging.debug("[%s] Getting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.ILLEGAL_MSG_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    if request_result["msg"] != "Device does not exist.":
        logging.error("[%s] Response contains wrong error message. "
                      % file_name
                      + "Server submitted data.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)