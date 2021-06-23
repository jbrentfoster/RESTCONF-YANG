"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import logging
from datetime import datetime
import os
import utils
import json
from distutils.dir_util import remove_tree
from distutils.dir_util import mkpath
import argparse


def main():
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    # Set up logging
    try:
        os.remove('collection.log')
    except Exception as err:
        logging.info("No log file to delete...")

    logFormatter = logging.Formatter('%(levelname)s:  %(message)s')
    rootLogger = logging.getLogger()
    rootLogger.level = logging.INFO

    fileHandler = logging.FileHandler(filename='collection.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    logging.info("Starting script...")
    current_time = str(datetime.now().strftime('%Y-%m-%d-%H%M-%S'))
    logging.info("Current time is: " + current_time)

    # Get path for collection files from command line arguments
    parser = argparse.ArgumentParser(description='A WAE collection tool for EPNM')
    parser.add_argument('-i', '--server_url', metavar='N', type=str, nargs='?',
                        help="Please provide the RESTCONF Server URL")
    parser.add_argument('-u', '--user', metavar='N', type=str, nargs='?',
                        help="Please provide the user name for the RESTCONF Server")
    parser.add_argument('-p', '--passwd', metavar='N', type=str, nargs='?',
                        help="Please provide the password for the RESTCONF Server")
    args = parser.parse_args()

    # base_url = 'http://cnc-il-ucs-haim2-onc.cisco.com/nbiservice'
    uri = '/restconf/data/ietf-yang-library:modules-state'

    logging.info("Cleaning files from last collection...")
    try:
        remove_tree('schema')
        os.remove('schema_links.txt')
    except Exception as err:
        logging.info("No files to cleanup...")
    # Recreate output directories
    mkpath('schema')

    yang_modules_dict = json.loads(utils.rest_get_json(args.server_url, uri, args.user, args.passwd))

    with open("schema_links.txt", 'w', encoding="utf8") as f:
        for module in yang_modules_dict['ietf-yang-library:modules-state']['module']:
            tmp_schema = module['schema'].replace("localhost:8008", "cnc-il-ucs-haim2-onc.cisco.com/nbiservice")
            f.write("{}{}".format(tmp_schema, "\n"))
        f.close()

    with open("schema_links.txt", 'r', encoding="utf8") as f:
        schema_links = f.readlines()
        schema_links = [x.strip() for x in schema_links]
        f.close()

    for link in schema_links:
        tmp_text = utils.rest_get_schema(link, "", args.user, args.passwd).strip()
        tmp_module = link.split("/")[-2]
        logging.info("Getting YANG schema for module: {}".format(tmp_module))
        with open("schema/{}.yang".format(tmp_module), 'w', encoding="utf8") as f:
            f.write(tmp_text)

    logging.info("Done!")


if __name__ == '__main__':
    main()
