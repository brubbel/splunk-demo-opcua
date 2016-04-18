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
x["measures"] = "O*:Windfarm_01:Turbine_01:Power"


y = dict()
y["name"] = "test"
y["connection"] = "opc.tcp://10.14.0.207:53530/OPCUA/SimulationServer"
y["username"] = "bill"
y["password"] = "monday"
y["connection_timeout"] = "30"
y["collect_duration"] = "5000"
y["measures"] = "O*:S*:S*"

z = dict()
z["name"] = "test"
z["connection"] = "opc.tcp://localhost:9966"
z["username"] = "bill"
z["password"] = "monday"
z["connection_timeout"] = "30"
z["measures"] = "O*:O*"
z["collect_duration"] = "5000"

def get_configs():
    return z
    #return y


utils.setup_logging = mock.MagicMock(side_effect=setup_logging)
import mi_opcua_subscription as mi_opcua

def test_mi_opcua_sub_run():
    mi_opcua.get_config = mock.MagicMock(side_effect=get_configs)
    patch("sys.stdin", StringIO("FOO"))
    patch("sys.stdout", new_callable=StringIO) 
        
    mi_opcua.run()
        

if __name__ == '__main__':
    test_mi_opcua_sub_run()
