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
    return logging.getLogger()

x = dict()
x["name"] = "test"
x["connection"] = "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"
x["connection_timeout"] = "30"
x["collect_duration"] = "5000"


y = dict()
y["name"] = "test"
y["connection"] = "opc.tcp://btsay-mbp15.local:53530/OPCUA/SimulationServer"
y["username"] = "bill"
y["password"] = "password"
y["connection_timeout"] = "30"
y["collect_duration"] = "1000"

def get_configs():
    return y
    #return y


utils.setup_logging = mock.MagicMock(side_effect=setup_logging)
import mi_opcua_event as mi_opcua

def test_mi_opcua_event_run():
    mi_opcua.get_config = mock.MagicMock(side_effect=get_configs)
    patch("sys.stdin", StringIO("FOO"))
    patch("sys.stdout", new_callable=StringIO) 
        
    mi_opcua.run()
        

if __name__ == '__main__':
    test_mi_opcua_event_run()
