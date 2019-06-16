#!/usr/bin/python3

import sys
import logging
import os
import time
import json
import binascii
from lib import *

'''
Tests a successful gps data submission, get view and device deletion.
'''

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    parse_config()

    device_name = __file__
    utctime_start = int(time.time()) - 10
    utctime_end = utctime_start + 9
    submitted_gps_data = list()
    keys = ["iv", "lat", "lon", "alt", "speed", "device_name", "utctime"]
    for i in range(10):
        iv = binascii.hexlify(os.urandom(16)).decode("utf-8")
        lat = binascii.hexlify(os.urandom(16)).decode("utf-8")
        lon = binascii.hexlify(os.urandom(16)).decode("utf-8")
        alt = binascii.hexlify(os.urandom(16)).decode("utf-8")
        speed = binascii.hexlify(os.urandom(16)).decode("utf-8")
        utctime = utctime_start + i
        gps_data = {"iv": iv,
                    "device_name": device_name,
                    "lat": lat,
                    "lon": lon,
                    "alt": alt,
                    "speed": speed,
                    "utctime": utctime}
        submitted_gps_data.append(gps_data)

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
        gps_data_recv = request_result["data"]["locations"][0]
        for key in keys:
            if gps_data_recv[key] != gps_data[key]:
                logging.error("[%s] Key '%s' contains wrong data."
                              % (file_name, key))
                logging.debug("[%s] Key '%s' contains: %s"
                              % (file_name, key, str(gps_data[key])))
                logging.debug("[%s] Json response: %s"
                              % (file_name, request_result))
                sys.exit(1)

    skip_start = 2
    frame_len = 5
    frame_start = utctime_start + skip_start
    frame_end = utctime_start + skip_start + frame_len - 1
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=view" \
               + "&device=" \
               + device_name \
               + "&start=" \
               + str(frame_start) \
               + "&end=" \
               + str(frame_end)

    # Get submitted data in timeframe and check received data.
    logging.debug("[%s] Getting gps data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    if len(request_result["data"]["locations"]) != frame_len:
        logging.error("[%s] Number of received data wrong. "
                      % file_name
                      + "Received %d, should have received %d."
                      % (len(request_result["data"]["locations"]), frame_len))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    for i in range(len(request_result["data"]["locations"])):
        gps_data_recv = request_result["data"]["locations"][i]
        for key in keys:
            idx = skip_start + i
            if gps_data_recv[key] != submitted_gps_data[idx][key]:
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
    logging.debug("[%s] Deleting gps device." % file_name)
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