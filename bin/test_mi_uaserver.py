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
x["name"] = "mi_uaserver:test"
x["description"] = "mi_uaserver:test"
x["count"] = "1"
x["interval"] = "5"
x["serverpath"] = "/splunk/uaserver"
x["namespace"] = "http://uaserver.splunk.com"
x["serverport"] = "9966"
x["nodefile"] = "meta.json"
x["datafile"] = "DataLog_2016_01.dat"

x["username"] = "bill"
x["password"] = "monday"
x["connection_timeout"] = "30"


def get_configs():
    return x

utils.setup_logging = mock.MagicMock(side_effect=setup_logging)

import mi_uaserver
mi_uaserver.get_config = mock.MagicMock(side_effect=get_configs)


def test_mi_uaserver_run():
    patch("sys.stdin", StringIO("FOO"))
    patch("sys.stdout", new_callable=StringIO) 
    mi_uaserver.run()
        

if __name__ == '__main__':
    test_mi_uaserver_run()