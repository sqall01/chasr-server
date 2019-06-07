#!/usr/bin/python3

import sys
import logging
import os
import time
import json
import binascii
from lib import *

'''
Tests a successful gps data submission and its deletion.
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

    # Submit data.
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

    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=last" \
               + "&device=" \
               + device_name

    # Get submitted data and check received data.
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

    # Delete submitted data.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/delete.php?mode=position" \
               + "&utctime=" \
               + str(utctime) \
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
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    data_same_ctr = 0
    if len(request_result["data"]) > 0:
        gps_data_recv = request_result["data"][0]
        keys = ["iv", "lat", "lon", "alt", "speed", "device_name", "utctime"]
        for key in keys:
            if gps_data_recv[key] == gps_data[key]:
                data_same_ctr += 1

        if data_same_ctr == len(keys):
            logging.error("[%s] Key '%s' contains same data. "
                          % (file_name, key)
                          + "Deleting failed.")
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
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    if len(request_result["data"]) > 0:
        logging.error("[%s] Response contains data. "
                      % file_name
                      + "Deleting device failed.")
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)