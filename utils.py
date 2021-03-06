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
import requests
import json
import logging
import urllib
from datetime import datetime


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def rest_get_json(baseURL, uri, user, password):
    requests.urllib3.disable_warnings()
    proxies = {
        "http": None,
        "https": None,
    }
    appformat = 'application/yang-data+json'
    headers = {'content-type': appformat, 'accept': appformat}
    if user == 'BEARER_TOKEN':
        auth = BearerAuth(password)
    else:
        auth = (user, password)
    # headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
    restURI = baseURL + uri
    try:
        r = requests.get(restURI, headers=headers, proxies=proxies, auth=auth, verify=False)
        # logging.info('The API response for URL {} is:\n{}'.format(restURI, json.dumps(r.json(), separators=(",",":"), indent=4)))
        if r.status_code == 200:
            return json.dumps(r.json(), indent=2)
        else:
            thejson = json.loads(json.dumps(r.json(), indent=2))
            errormessage = thejson.get('rc.errors').get('error').get('error-message')
            logging.info('error message is: ' + errormessage)
            raise errors.InputError(restURI, "HTTP status code: " + str(r.status_code),
                                    "Error message returned: " + errormessage)
    except Exception as err:
        # logging.error('Exception raised: ' + str(type(err)) + '\nURL: {}\n{}\n{}'.format(err.expression, err.statuscode,err.message))
        return


def rest_get_schema(baseURL, uri, user, password):
    requests.urllib3.disable_warnings()
    proxies = {
        "http": None,
        "https": None,
    }
    appformat = 'application/yang'
    headers = {'accept': appformat}
    restURI = baseURL + uri
    if user == 'BEARER_TOKEN':
        auth = BearerAuth(password)
    else:
        auth = (user, password)
    try:
        r = requests.get(restURI, headers=headers, proxies=proxies, auth=auth, verify=False)
        # logging.info('The API response for URL {} is:\n{}'.format(restURI, json.dumps(r.json(), separators=(",",":"), indent=4)))
        if r.status_code == 200:
            return r.text
        #     return json.dumps(r.json(), indent=2)
        # else:
        #     thejson = json.loads(json.dumps(r.json(), indent=2))
        #     errormessage = thejson.get('rc.errors').get('error').get('error-message')
        #     logging.info('error message is: ' + errormessage)
        #     raise errors.InputError(restURI, "HTTP status code: " + str(r.status_code), "Error message returned: " + errormessage)
    except Exception as err:
        logging.error('Exception raised: ' + str(type(err)) + '\nURL: {}\n{}\n{}'.format(err.expression, err.statuscode,err.message))
        return


def rest_post_json(baseURL, uri, thejson, user, password):
    requests.urllib3.disable_warnings()
    proxies = {
        "http": None,
        "https": None,
    }
    appformat = 'application/yang-data+json'
    headers = {'content-type': appformat, 'accept': appformat}
    restURI = baseURL + uri
    try:
        r = requests.post(restURI, data=thejson, headers=headers, proxies=proxies, auth=(user, password), verify=False)
        # logging.info('The API response for URL {} is:\n{}'.format(restURI, json.dumps(r.json(), separators=(",",":"), indent=4)))
        if r.status_code == 200:
            return json.dumps(r.json(), indent=2)
        else:
            thejson = json.loads(json.dumps(r.json(), indent=2))
            errormessage = thejson.get('rc.errors').get('error').get('error-message')
            logging.info('error message is: ' + errormessage)
            raise errors.InputError(restURI, "HTTP status code: " + str(r.status_code),
                                    "Error message returned: " + errormessage)
    except Exception as err:
        logging.error('Exception raised: ' + str(type(err)) + '\nURL: {}\n{}\n{}'.format(err.expression, err.statuscode,
                                                                                         err.message))
        return
