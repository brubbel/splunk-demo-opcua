'''
Created on Jan 12, 2016

@author: btsay
'''
#import os
#os.environ["SPLUNK_HOME"] = "/home/btsay/Documents/splunk/"


import splunk_opcua.utils as utils
logger = utils.setup_logging("opcua")

import sys
from collections import OrderedDict as odict
import signal

from opcua import Client
from splunk_opcua import mi
from splunk_opcua.ua import node

SCHEME = """
<scheme>
    <title>OPC UA Subscription</title>
    <description>Manage the data subscription from OPC UA Server.</description>
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

            <arg name="collect_duration">
                <title>Collect Duration</title>
                <description> Collection duration in milliseconds.</description>
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
            
        </args>
    </endpoint>
</scheme>

"""


class SubHandler(object):
    def __init__(self, stanza):
        self.stanza = stanza
    
    """
    Client to subscription. It will receive events from server
    """
    def datachange_notification(self, node, val, data):
        out = sys.stdout
        mi.init_stream(out)
        
        try:
            evt = odict()  # use ordered dict to keep order of values.
            evt["stanza"] = self.stanza
            evt["collect_time"] = mi.current_milliseconds()
            evt["node_id"] = node.nodeid.Identifier
            evt["measure"] = node.get_display_name().Text
            evt["status"] = data.monitored_item.Value.StatusCode.name
            evt["data_type"] = data.monitored_item.Value.Value.VariantType.name
            evt["value"] = utils.format_float(val) if isinstance(val, float) else val
            mi.print_kv_event(self.stanza, evt["collect_time"], evt, out)
            logger.info("Subscribing measure : %s" % evt["measure"])
        except Exception as ex:
            logger.critical(ex)
        finally:
            mi.fini_stream(out)
        
    def event_notification(self, event):
        logger.info("Subscription: New event %s " % event)
        print event



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


def run():
    logger.info("Modular Input mi_opcua_subscription command: %s" % sys.argv)
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
        logger.info("Modular Input mi_opcua_subscription Starts data collection.")
        
        configs = get_config()
        stanza = configs["name"]
        # server_uri = configs["server_uri"]
        # sessionKey = configs["session_key"]
        # userName = "admin"   # make this modular input as application context only.
        patterns = configs["measures"].split(":")
        tout = configs["connection_timeout"].strip()
        timeout = 1 if len(tout) <= 0 else int(tout)
        ct = configs["collect_duration"].strip()
        duration = 1000 if len(ct) <=0 else int(ct)
        
        conn = configs["connection"]   ## "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"

        if configs.has_key("username"):
            username = configs["username"].strip()
            if len(username)>0:
                password = configs["password"].strip()
                conn = "%s?username=%s&password=%s" % (conn, username, password)
    
        client = Client(conn, timeout=timeout)
        
        try:
            client.connect()
            measures = []
            root = client.get_root_node()
            
            node.collect_measures(measures, patterns, root)
            
            subscribers = []
            for m in measures:
                try:
                    subscribers.append(m[len(m)-1])
                except:
                    logger.warn("The node of %s is invalid to subscribe." % m)
                    
            handler = SubHandler(stanza)
            sub = client.create_subscription(duration, handler)
            dchandle = sub.subscribe_data_change(subscribers)
       
            def signal_handler(signal, frame):
                logger.info('Press Ctrl+C')
                
                if signal in [signal.SIGABRT, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM]:
                    sub.unsubscribe(dchandle)
                    sub.delete()
                    client.disconnect()

            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGABRT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            signal.signal(signal.SIGQUIT, signal_handler)

            signal.pause()
                            
        except Exception as ex:
            logger.critical(ex)
        finally:
            sub.unsubscribe(dchandle)
            sub.delete()
            client.disconnect()
            
            logger.info("---- end of sub opc ua ----")

if __name__ == '__main__':
    logger.info("---- sub opc ua ----")
    try:
        run()
    except Exception as ex:
        logger.critical(ex)

