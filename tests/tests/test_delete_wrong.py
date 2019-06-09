#!/usr/bin/python3

import sys
import logging
import os
import time
import json
import binascii
from lib import *

'''
Tests error handling for wrong given delete parameter.
'''

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    parse_config()

    device_name = __file__
    iv = binascii.hexlify(os.urandom(16)).decode("utf-8")
    lat = binascii.hexlify(os.urandom(16)).decode("utf-8")
    lon = binascii.hexlify(os.urandom(16)).decode("utf-8")
    alt = binascii.hexlify(os.urandom(16)).decode("utf-8")
    speed = binascii.hexlify(os.urandom(16)).decode("utf-8")
    utctime = int(time.time())
    gps_data = {"iv": iv,
                "device_name": device_name,
                "lat": lat,
                "lon": lon,
                "alt": alt,
                "speed": speed,
                "utctime": utctime}

    # Submit test data.
    payload = {"user": Settings.username,
               "password": Settings.password,
               "gps_data": json.dumps([gps_data])}
    logging.debug("[%s] Submitting gps data." % file_name)
    request_result = send_post_request("/submit.php", payload, file_name)
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    # Wrong mode.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/delete.php?mode=position_wrong"
    logging.debug("[%s] Deleting gps data." % file_name)
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
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    gps_data_recv = request_result["data"][0]
    for key in ["iv", "lat", "lon", "alt", "speed", "device_name", "utctime"]:
        if gps_data_recv[key] != gps_data[key]:
            logging.error("[%s] Key '%s' contains wrong data."
                          % (file_name, key))
            logging.debug("[%s] Key '%s' contains: %s"
                          % (file_name, key, str(gps_data[key])))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

    # Missing device for mode "position".
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/delete.php?mode=position" \
               + "&utctime=" \
               + str(utctime)
    logging.debug("[%s] Deleting gps data." % file_name)
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
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    gps_data_recv = request_result["data"][0]
    for key in ["iv", "lat", "lon", "alt", "speed", "device_name", "utctime"]:
        if gps_data_recv[key] != gps_data[key]:
            logging.error("[%s] Key '%s' contains wrong data."
                          % (file_name, key))
            logging.debug("[%s] Key '%s' contains: %s"
                          % (file_name, key, str(gps_data[key])))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

    # Missing utctime for mode "position".
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/delete.php?mode=position" \
               + "&device=" \
               + device_name
    logging.debug("[%s] Deleting gps data." % file_name)
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
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    gps_data_recv = request_result["data"][0]
    for key in ["iv", "lat", "lon", "alt", "speed", "device_name", "utctime"]:
        if gps_data_recv[key] != gps_data[key]:
            logging.error("[%s] Key '%s' contains wrong data."
                          % (file_name, key))
            logging.debug("[%s] Key '%s' contains: %s"
                          % (file_name, key, str(gps_data[key])))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

    # Missing device for mode "device".
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/delete.php?mode=device"
    logging.debug("[%s] Deleting gps data." % file_name)
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
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    gps_data_recv = request_result["data"][0]
    for key in ["iv", "lat", "lon", "alt", "speed", "device_name", "utctime"]:
        if gps_data_recv[key] != gps_data[key]:
            logging.error("[%s] Key '%s' contains wrong data."
                          % (file_name, key))
            logging.debug("[%s] Key '%s' contains: %s"
                          % (file_name, key, str(gps_data[key])))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

    # Delete device for clean up.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/delete.php?mode=device" \
               + "&device=" \
               + device_name
    logging.debug("[%s] Deleting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.NO_ERROR:
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
                      + "Deleting device failed.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)