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
import mi_uaserver2 as mi_uaserver

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
x["name"] = "UA Simulator II"
x["description"] = "UA Simulator II"
x["interval"] = "5"
x["serverpath"] = "/splunk/uaserver2"
x["namespace"] = "http://uaserver2.splunk.com"
x["serverport"] = "9988"
x["nodefile"] = "meta.json"

x["username"] = "bill"
x["password"] = "monday"
x["connection_timeout"] = "30"


def get_configs():
    return x

utils.setup_logging = mock.MagicMock(side_effect=setup_logging)

mi_uaserver.get_config = mock.MagicMock(side_effect=get_configs)


def test_mi_uaserver_run():
    patch("sys.stdin", StringIO("FOO"))
    patch("sys.stdout", new_callable=StringIO) 
    mi_uaserver.run()
        

if __name__ == '__main__':
    test_mi_uaserver_run()