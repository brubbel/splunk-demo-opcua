'''
Created on Jan 12, 2016

@author: btsay
'''
#import os
#os.environ["SPLUNK_HOME"] = "/home/btsay/Documents/splunk/"

import logging

import splunk_opcua.utils as utils
logger = utils.setup_logging("opcua")

import os
import uaserver as ua
import json
import sys
from collections import OrderedDict as odict

from opcua import Client
from splunk_opcua import mi
from splunk_opcua.ua import node

SCHEME = """
<scheme>
    <title>OPC UA Pull Connect</title>
    <description>Manage the data collection from OPC UA Server.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>

    <endpoint>
        <args>

            <arg name="connection">
                <title>OPC Server Connection</title>
                <description> connection parameters to access OPC server.</description>
            </arg>

            <arg name="username">
                <title>OPC Server Login User</title>
                <description> Login User to access OPC server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="password">
                <title>OPC Server Login Password</title>
                <description> Login Password to access OPC server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="connection_timeout">
                <title>OPC Server Connection Timeout</title>
                <description> connection Timeout to access OPC server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="description">
                <title>Descrption</title>
                <description>Description for this data collector.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="measures">
                <title>Measure Setups</title>
                <description>Resources to collect from, can be wild cards.</description>
            </arg>

            <arg name="metrics_spec">
                <title>Metrics Specification</title>
                <description>Specification for metrics to display.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            
        </args>
    </endpoint>
</scheme>

"""


def do_scheme():
    print (SCHEME)

def usage():
    print ("usage: %s [--scheme|--validate-arguments]")
    utils.os_specific_sys_exit(2)
    
def test():
    pass
    
def validate_arguments():
    pass

def get_config():
    config_str = sys.stdin.read()
    return utils.get_config(config_str)


def collect_data(stanza, measure, spec={}):
    out = sys.stdout

    try:
        #obj = symbol.join(m)
        data = measure.get_data_value()
        evt = odict()  # use ordered dict to keep order of values.
        evt["stanza"] = stanza
        evt["collect_time"] = str(data.SourceTimestamp)
        evt["node_id"] = measure.nodeid.Identifier
        evt["measure"] = measure.get_display_name().Text
        evt["status"] = data.StatusCode.name
        evt["data_type"] = data.Value.VariantType.name
        evt["value"] = utils.format_float(data.Value.Value)
        
        if spec.has_key(evt["measure"]):
            m = spec[evt["measure"]]
            evt["unit"] = m["unit"]
            evt["asset"] = m["asset"]
            evt["metric"] = m["metric"]
            if m.has_key("optimum"):
                evt["optimum"] = m["optimum"]
                
            evt["demo"] = "True"
        
        mi.print_kv_event(stanza, evt["collect_time"], evt, out)
        logger.info("Collecting measure : %s" % evt["measure"])
    except Exception as ex:
        logger.critical(ex)

def run():
    logger.info("Modular Input mi_opcua command: %s" % sys.argv)
    if len(sys.argv) > 1:
        try:
            if sys.argv[1] == "--scheme":
                do_scheme()
            elif sys.argv[1] == "--validate-arguments":
                validate_arguments()
            elif sys.argv[1] == "--test":
                test()
            else:
                usage()
        except Exception as ex:
            logger.critical(ex)
    else:
        logger.info("Modular Input mi_opcua Starts data collection.")
        
        configs = get_config()
        stanza = configs["name"]
        patterns = configs["measures"].split(":")
        tout = configs["connection_timeout"].strip()
        spec = configs["metrics_spec"].strip()
        timeout = 1 if len(tout) <= 0 else int(tout)

        conn = configs["connection"]   ## "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"

        if configs.has_key("username"):
            username = configs["username"].strip()
            if len(username)>0:
                password = configs["password"].strip()
                conn = "%s?username=%s&password=%s" % (conn, username, password)
    
        client = Client(conn, timeout=timeout)

        mi.init_stream(sys.stdout)
        try:
            logger.info("Start connecting OPC Server [%s]." % conn)
            client.connect()
            logger.info("OPC Server [%s] is connected." % conn)
            measures = []
            root = client.get_root_node()
            
            node.collect_measures(measures, patterns, root)
            
            md = {}
            try:
                jm = os.path.join(ua.data_dir(), spec)
                with open(jm, 'r') as mfp:
                    md = json.load(mfp)
                    mfp.close()
            except:
                pass

            for m in measures:
                collect_data(stanza, m[len(m)-1], spec=md)
                
        except Exception as ex:
            logger.critical(ex)
        finally:
            mi.fini_stream(sys.stdout)
            logger.info("---- end of opc ua ----")
            client.disconnect()

if __name__ == '__main__':
    logger.info("---- opc ua ----")
    try:
        run()
    except Exception as ex:
        logger.critical(ex)




