'''
Created on Jan 19, 2016

@author: btsay
'''

import logging
import mock
from mock import patch
from StringIO import StringIO

import splunk_opcua.utils as utils

import os
import mi_iot_event_gen as mi_iot

os.environ["SPLUNK_HOME"] = "/home/btsay/Documents/splunk"
os.environ["SPLUNK_DB"] = "/home/btsay/Documents/splunk/db"

def setup_logging(app, level=logging.INFO):
    return logging.getLogger(app)


'''
description = <value>
serverpath = <value>
namespace = <value>
serverport = <value>
nodefile = <value>
datafile = <value>
username = <value>
password = <value>
connection_timeout = <value>
'''


x = dict()
x["name"] = "IoT Event Generation"
x["description"] = "IoT Event Generation"
x["interval"] = "5"
x["assets"] = "assets.json"
x["metrics"] = "metrics2.json"
x["conditions"] = "conditions.json"


def get_configs():
    return x

utils.setup_logging = mock.MagicMock(side_effect=setup_logging)

mi_iot.get_config = mock.MagicMock(side_effect=get_configs)


def test_mi_iot_evtgen_run():
    patch("sys.stdin", StringIO("FOO"))
    patch("sys.stdout", new_callable=StringIO) 
    mi_iot.run()
        

if __name__ == '__main__':
    test_mi_iot_evtgen_run()