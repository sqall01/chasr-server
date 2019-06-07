#!/usr/bin/python3

import sys
import logging
import os
import time
import json
import binascii
from lib import *

'''
Tests successful gps data submission, get devices
and device deletion.
'''

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    parse_config()

    num_devices = 10
    device_name = __file__
    utctime_start = int(time.time()) - num_devices
    utctime_end = utctime_start + 9
    submitted_gps_data = list()
    keys = ["iv", "lat", "lon", "alt", "speed", "device_name", "utctime"]
    for i in range(num_devices):
        iv = binascii.hexlify(os.urandom(16)).decode("utf-8")
        lat = binascii.hexlify(os.urandom(16)).decode("utf-8")
        lon = binascii.hexlify(os.urandom(16)).decode("utf-8")
        alt = binascii.hexlify(os.urandom(16)).decode("utf-8")
        speed = binascii.hexlify(os.urandom(16)).decode("utf-8")
        utctime = utctime_start + i
        curr_device_name = device_name + "_" + str(i)
        gps_data = {"iv": iv,
                    "device_name": curr_device_name,
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

    # Get devices and check received data.
    payload = {"user": Settings.username,
               "password": Settings.password}
    location = "/get.php?mode=devices"
    logging.debug("[%s] Getting devices data." % file_name)
    request_result = send_post_request(location, payload, file_name)
    if request_result["code"] != ErrorCodes.NO_ERROR:
        logging.error("[%s] Service error code: %d."
                      % (file_name, request_result["code"]))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)

    device_data_recv = request_result["data"]

    if len(device_data_recv) != num_devices:
        logging.error("[%s] Number of devices wrong."
                      % file_name)
        logging.error("[%s] Submitted %d and received %d."
                      % (file_name, num_devices, len(device_data_recv)))
        logging.debug("[%s] Json response: %s"
                      % (file_name, request_result))
        sys.exit(1)
    for i in range(num_devices):

        gps_data_recv = device_data_recv[i]

        curr_device_name = device_name + "_" + str(i)
        if curr_device_name != gps_data_recv["device_name"]:
            logging.error("[%s] Device name '%s' wrong data."
                          % (file_name, gps_data_recv["device_name"]))
            logging.error("[%s] Device name '%s' instead of '%s'."
                          % (file_name, gps_data_recv["device_name"],
                            curr_device_name))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

    # Delete all gps devices.
    for i in range(num_devices):

        # Delete devices for clean up.
        curr_device_name = device_name + "_" + str(i)
        payload = {"user": Settings.username,
                   "password": Settings.password}
        location = "/delete.php?mode=device" \
                   + "&device=" \
                   + curr_device_name
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
    location = "/get.php?mode=devices"
    logging.debug("[%s] Getting devices data." % file_name)
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