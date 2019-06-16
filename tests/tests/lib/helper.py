#!/usr/bin/python3

# written by sqall
# twitter: https://twitter.com/sqall01
# blog: https://h4des.org/blog
# github: https://github.com/sqall01
# 
# Licensed under the GNU Affero General Public License, version 3.

import configparser
import logging
import sys
import os
import requests

class ErrorCodes:
    NO_ERROR = 0
    DATABASE_ERROR = 1
    AUTH_ERROR = 2
    ILLEGAL_MSG_ERROR = 3
    SESSION_EXPIRED = 4
    ACL_ERROR = 5

class Settings:
    server = None
    num_min_devices = None
    num_mid_devices = None
    num_max_devices = None
    username_max_devices = None
    password_max_devices = None
    username_mid_devices = None
    password_mid_devices = None
    username_no_acl = None
    password_no_acl = None
    valid_cert = None

# Function creates a path location for the given user input.
def make_path(input_location, curr_location=__file__):
    # Do nothing if the given location is an absolute path.
    if input_location[0] == "/":
        return input_location
    # Replace ~ with the home directory.
    elif input_location[0] == "~":
        return os.environ["HOME"] + input_location[1:]
    # Assume we have a given relative path.
    return os.path.dirname(os.path.abspath(curr_location)) \
           + "/" \
           + input_location

# Parse configuration file.
def parse_config():

    # Parse logging settings from config file.
    config = None
    file_name = os.path.basename(__file__)
    try:
        config = configparser.RawConfigParser(allow_no_value=False)
        config.read([make_path("../../config/config.conf")])

        # Parse logging settings.
        if config.get("general", "loglevel").upper() == "DEBUG":
            loglevel = logging.DEBUG
        elif config.get("general", "loglevel").upper() == "INFO":
            loglevel = logging.INFO
        elif config.get("general", "loglevel").upper() == "WARNING":
            loglevel = logging.WARNING
        elif config.get("general", "loglevel").upper() == "ERROR":
            loglevel = logging.ERROR
        elif config.get("general", "loglevel").upper() == "CRITICAL":
            loglevel = logging.CRITICAL
        else:
            raise ValueError("No valid log level in config file.")

        # Initialize logging.
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', 
            datefmt='%m/%d/%Y %H:%M:%S', level=loglevel)

    except Exception as e:
        print("Could not parse configuration file.")
        print(e)
        sys.exit(1)

    # Parse settings from config file.
    try:
        Settings.server = config.get("general", "server")
        Settings.num_min_devices = config.getint("general", "num_min_devices")
        Settings.num_mid_devices = config.getint("general", "num_mid_devices")
        Settings.num_max_devices = config.getint("general", "num_max_devices")
        Settings.username_max_devices = config.get("general",
                                                   "username_max_devices")
        Settings.password_max_devices = config.get("general",
                                                   "password_max_devices")
        Settings.username_mid_devices = config.get("general",
                                                   "username_mid_devices")
        Settings.password_mid_devices = config.get("general",
                                                   "password_mid_devices")
        Settings.username_no_acl = config.get("general",
                                              "username_no_acl")
        Settings.password_no_acl = config.get("general",
                                              "password_no_acl")
        Settings.valid_cert = config.getboolean("general", "valid_cert")
    except:
        logging.exception("[%s] Failed parsing config file" % file_name)
        sys.exit(1)

def send_post_request(server_location, payload, file_name, session=None):

    if not session:
        session = requests.Session()

    try:
        r = session.post(Settings.server
                          + server_location,
                          verify=Settings.valid_cert,
                          data=payload)
    except:
        logging.exception("[%s] Failed to send POST request."
                          % file_name)
        sys.exit(1)

    if r.status_code != 200:
        logging.error("[%s]: Unable to submit data. "
                      % file_name
                      + "Server status code: %d."
                      % r.status_code)
        sys.exit(1)

    # Parse response.
    try:
        request_result = r.json()
    except:
        logging.exception("[%s] Failed to decode json response."
                          % file_name)
        logging.debug("[%s] Json response: %s"
                      % (file_name, r.text))
        sys.exit(1)

    return request_result