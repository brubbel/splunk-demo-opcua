'''
Created on Jan 19, 2016

@author: btsay
'''

import logging
import mock
from mock import patch
from StringIO import StringIO

import splunk_opcua.utils as utils

def setup_logging(app, level=logging.INFO):
    return logging.getLogger(app)


x = dict()
x["name"] = "test"
x["connection"] = "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"
x["connection_timeout"] = "30"
x["measures"] = "O*:W*04:T*:T*"


y = dict()
y["name"] = "test"
y["connection"] = "opc.tcp://10.1.10.46:53530/OPCUA/SimulationServer"
y["username"] = "bill"
y["password"] = "monday"
y["connection_timeout"] = "30"
y["measures"] = "O*:S*:S*"

z = dict()
z["name"] = "test"
z["connection"] = "opc.tcp://localhost:9988"
z["username"] = "bill"
z["password"] = "monday"
z["metrics_spec"] = "metrics2.json"
z["connection_timeout"] = "30"
z["measures"] = "O*:~Ser*"

'''
import urlparse

print urlparse.urlparse(y["connection"])
'''

def get_configs():
    return z
    #return y


utils.setup_logging = mock.MagicMock(side_effect=setup_logging)

import mi_opcua
mi_opcua.get_config = mock.MagicMock(side_effect=get_configs)


def test_mi_opcua_run():
    patch("sys.stdin", StringIO("FOO"))
    patch("sys.stdout", new_callable=StringIO) 
    mi_opcua.run()
        

if __name__ == '__main__':
    test_mi_opcua_run()