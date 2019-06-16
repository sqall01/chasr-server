#!/usr/bin/python3

import sys
import logging
import os
import time
import json
import binascii
from lib import *

'''
Tests a successful gps data submission, the acl for number of devices
and its deletion.
'''

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    parse_config()


    all_test_settings = list()
    all_test_settings.append({"num_devices": Settings.num_min_devices,
                              "username": Settings.username_no_acl,
                              "password": Settings.password_no_acl})
    all_test_settings.append({"num_devices": Settings.num_mid_devices,
                              "username": Settings.username_mid_devices,
                              "password": Settings.password_mid_devices})
    all_test_settings.append({"num_devices": Settings.num_max_devices,
                              "username": Settings.username_max_devices,
                              "password": Settings.password_max_devices})

    for test_settings in all_test_settings:
        num_devices = test_settings["num_devices"]
        username = test_settings["username"]
        password = test_settings["password"]

        # Get all existing devices and delete them for clean up.
        payload = {"user": username,
                   "password": password}
        location = "/get.php?mode=devices"
        logging.debug("[%s] Getting devices data." % file_name)
        request_result = send_post_request(location, payload, file_name)
        if request_result["code"] != ErrorCodes.NO_ERROR:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)
        device_data_recv = request_result["data"]["devices"]
        for device_dict in device_data_recv:
            payload = {"user": username,
                       "password": password}
            location = "/delete.php?mode=device" \
                       + "&device=" \
                       + device_dict["device_name"]
            logging.debug("[%s] Deleting gps device." % file_name)
            request_result = send_post_request(location, payload, file_name)
            if request_result["code"] != ErrorCodes.NO_ERROR:
                logging.error("[%s] Used username '%s'."
                              % (file_name, username))
                logging.error("[%s] Service error code: %d."
                              % (file_name, request_result["code"]))
                logging.debug("[%s] Json response: %s"
                              % (file_name, request_result))
                sys.exit(1)

        device_name = __file__
        utctime_start = int(time.time()) - Settings.num_min_devices
        submitted_gps_data = list()
        for i in range(num_devices):
            iv = binascii.hexlify(os.urandom(16)).decode("utf-8")
            lat = binascii.hexlify(os.urandom(16)).decode("utf-8")
            lon = binascii.hexlify(os.urandom(16)).decode("utf-8")
            alt = binascii.hexlify(os.urandom(16)).decode("utf-8")
            speed = binascii.hexlify(os.urandom(16)).decode("utf-8")
            utctime = utctime_start + i
            curr_device_name = device_name + "_%09d" % i
            gps_data = {"iv": iv,
                        "device_name": curr_device_name,
                        "lat": lat,
                        "lon": lon,
                        "alt": alt,
                        "speed": speed,
                        "utctime": utctime}

            # Submit data.
            payload = {"user": username,
                       "password": password,
                       "gps_data": json.dumps([gps_data])}
            logging.debug("[%s] Submitting gps data." % file_name)
            request_result = send_post_request("/submit.php", payload, file_name)
            if request_result["code"] != ErrorCodes.NO_ERROR:
                logging.error("[%s] Used username '%s'."
                              % (file_name, username))
                logging.error("[%s] Service error code: %d."
                              % (file_name, request_result["code"]))
                logging.debug("[%s] Json response: %s"
                              % (file_name, request_result))
                sys.exit(1)

        # Get devices and check received data.
        payload = {"user": username,
                   "password": password}
        location = "/get.php?mode=devices"
        logging.debug("[%s] Getting devices data." % file_name)
        request_result = send_post_request(location, payload, file_name)
        if request_result["code"] != ErrorCodes.NO_ERROR:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        device_data_recv = request_result["data"]["devices"]

        if len(device_data_recv) != num_devices:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] Number of devices wrong."
                          % file_name)
            logging.error("[%s] Submitted %d and received %d."
                          % (file_name, num_devices, len(device_data_recv)))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)
        for i in range(num_devices):

            gps_data_recv = device_data_recv[i]

            curr_device_name = device_name + "_%09d" % i
            if curr_device_name != gps_data_recv["device_name"]:
                logging.error("[%s] Used username '%s'."
                              % (file_name, username))
                logging.error("[%s] Device name '%s' wrong data."
                              % (file_name, gps_data_recv["device_name"]))
                logging.error("[%s] Device name '%s' instead of '%s'."
                              % (file_name, gps_data_recv["device_name"],
                                curr_device_name))
                logging.debug("[%s] Json response: %s"
                              % (file_name, request_result))
                sys.exit(1)

        # Add additional device which is more than the allowed number.
        iv = binascii.hexlify(os.urandom(16)).decode("utf-8")
        lat = binascii.hexlify(os.urandom(16)).decode("utf-8")
        lon = binascii.hexlify(os.urandom(16)).decode("utf-8")
        alt = binascii.hexlify(os.urandom(16)).decode("utf-8")
        speed = binascii.hexlify(os.urandom(16)).decode("utf-8")
        utctime = utctime_start + num_devices
        forbidden_device_name = device_name + "_%09d" % num_devices
        gps_data = {"iv": iv,
                    "device_name": forbidden_device_name,
                    "lat": lat,
                    "lon": lon,
                    "alt": alt,
                    "speed": speed,
                    "utctime": utctime}

        # Submit data.
        payload = {"user": username,
                   "password": password,
                   "gps_data": json.dumps([gps_data])}
        logging.debug("[%s] Submitting gps data." % file_name)
        request_result = send_post_request("/submit.php", payload, file_name)
        if request_result["code"] != ErrorCodes.ACL_ERROR:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] ACL error expected. Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        # Get devices and check additional device was not added.
        payload = {"user": username,
                   "password": password}
        location = "/get.php?mode=devices"
        logging.debug("[%s] Getting devices data." % file_name)
        request_result = send_post_request(location, payload, file_name)
        if request_result["code"] != ErrorCodes.NO_ERROR:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        device_data_recv = request_result["data"]["devices"]

        if len(device_data_recv) != num_devices:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] Number of devices wrong "
                          % file_name
                          + "after forbidden submission.")
            logging.error("[%s] Allowed devices %d and received %d."
                          % (file_name, num_devices, len(device_data_recv)))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)

        for device_recv in device_data_recv:
            if device_recv["device_name"] == forbidden_device_name:
                logging.error("[%s] Used username '%s'."
                              % (file_name, username))
                logging.error("[%s] Forbidden device '%s' received."
                              % (file_name, forbidden_device_name))
                logging.debug("[%s] Json response: %s"
                              % (file_name, request_result))
                sys.exit(1)

        # Delete all gps devices for clean up.
        for i in range(num_devices):

            # Delete devices for clean up.
            curr_device_name = device_name + "_%09d" % i
            payload = {"user": username,
                       "password": password}
            location = "/delete.php?mode=device" \
                       + "&device=" \
                       + curr_device_name
            logging.debug("[%s] Deleting gps device." % file_name)
            request_result = send_post_request(location, payload, file_name)
            if request_result["code"] != ErrorCodes.NO_ERROR:
                logging.error("[%s] Used username '%s'."
                              % (file_name, username))
                logging.error("[%s] Service error code: %d."
                              % (file_name, request_result["code"]))
                logging.debug("[%s] Json response: %s"
                              % (file_name, request_result))
                sys.exit(1)

        # Get submitted data and check received data.
        payload = {"user": username,
                   "password": password}
        location = "/get.php?mode=devices"
        logging.debug("[%s] Getting devices data." % file_name)
        request_result = send_post_request(location, payload, file_name)
        if request_result["code"] != ErrorCodes.NO_ERROR:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] Service error code: %d."
                          % (file_name, request_result["code"]))
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)
        if len(request_result["data"]["devices"]) > 0:
            logging.error("[%s] Used username '%s'."
                          % (file_name, username))
            logging.error("[%s] Response contains data. "
                          % file_name
                          + "Deleting device failed.")
            logging.debug("[%s] Json response: %s"
                          % (file_name, request_result))
            sys.exit(1)