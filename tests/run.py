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
import subprocess
import time
from tests import *

timeout = 30

if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    test_dir = make_path("tests/", __file__)
    parse_config()

    # Find all test cases.
    tests_list = list()
    tests_failed_list = list()
    for element in os.listdir(test_dir):
        if element[-3:] == ".py" and element.startswith("test_"):
            tests_list.append(element)
    tests_list.sort()

    logging.info("[%s] Found %d test cases."
                 % (file_name, len(tests_list)))

    start_time = time.time()

    # Execute test cases.
    for ctr in range(len(tests_list)):
        logging.info("[%s] Executing test case %d/%d."
                     % (file_name, ctr+1, len(tests_list)))

        test_case = tests_list[ctr]
        try:
            os.chmod(test_dir + test_case, 0o700)
            process = subprocess.Popen([test_dir + test_case])
        except:
            logging.exception("[%s] Failed to execute test case."
                              % file_name)
            tests_failed_list.append(test_case)
            continue

        test_start_time = time.time()
        while True:
            exit_code = process.poll()

            if (test_start_time + timeout) < time.time():
                logging.error("[%s] Test case timeout. Terminating it."
                              % file_name)
                process.terminate()
                time.sleep(1)
                exit_code = process.poll()
                if exit_code != 15:
                    process.kill()
                break

            if exit_code is None:
                time.sleep(0.5)
                continue
            break
        if exit_code != 0:
            logging.warning("[%s] Test case failed."
                            % file_name)
            tests_failed_list.append(test_case)
        else:
            logging.info("[%s] Test case successful."
                         % file_name)

    # Summary.
    num_succ = len(tests_list)-len(tests_failed_list)
    logging.info("[%s] %d/%d test cases successful."
                 % (file_name, num_succ, len(tests_list)))