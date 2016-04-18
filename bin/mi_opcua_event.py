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
from splunk_opcua import mi
from opcua import Client
from splunk_opcua.ua import node

SCHEME = """
<scheme>
    <title>OPC UA Event Notification</title>
    <description>Manage All Event notifications from OPC UA Server.</description>
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

             <!--
            <arg name="events">
                <title>Events</title>
                <description>Events to collect from, can be wild cards.</description>
            </arg>

            <arg name="event_types">
                <title>Event Types</title>
                <description>Event types to collect from, can be wild cards.</description>
            </arg>
            
            -->
        </args>
    </endpoint>
</scheme>

"""



class SubHandler(object):
    def __init__(self, stanza):
        self.stanza = stanza
    
    """
    def datachange_notification(self, node, val, data):
        out = sys.stdout
        mi.init_stream(out)
        
        try:
            evt = odict()  # use ordered dict to keep order of values.
            evt["stanza"] = self.stanza
            evt["collect_time"] = mi.current_milliseconds()
            evt["measure"] = node.nodeid.Identifier
            evt["status"] = data.monitored_item.Value.StatusCode.name
            evt["data_type"] = data.monitored_item.Value.Value.VariantType.name
            evt["value"] = val
            mi.print_kv_event(self.stanza, evt["collect_time"], evt, out)
            logger.info("Subscribing measure : %s" % evt["measure"])
        except Exception as ex:
            logger.critical(ex)
        finally:
            mi.fini_stream(out)
    """
    
    
    def event_notification(self, event):
        out = sys.stdout
        mi.init_stream(out)
        
        try:
            evt = odict()  # use ordered dict to keep order of values.
            evt["stanza"] = self.stanza
            
            evt["EventType"] = node.get_event_type(event.EventType.Identifier)
            
            if hasattr(event, "ReceiveTime"):
                evt["ReceiveTime"] = str(event.ReceiveTime)

            if hasattr(event, "Time"):
                evt["Time"] = str(event.Time)
                
            evt["Severity"] = event.Severity
            
            if hasattr(event, "SourceName"):
                evt["SourceName"] = event.SourceName
                
            evt["SourceNode"] = event.SourceNode.Identifier
            evt["collect_time"] = mi.current_milliseconds()
            evt["Message"] = event.Message.Text
            mi.print_kv_event(self.stanza, evt["collect_time"], evt, out)
            logger.info("SourceNode %s Notified : %s." % (evt["SourceNode"], evt["Message"]))
        except Exception as ex:
            logger.critical(ex)
        finally:
            mi.fini_stream(out)


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
    logger.info("Modular Input mi_opcua_event command: %s" % sys.argv)
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
        logger.info("Modular Input mi_opcua_event Starts data collection.")
        
        configs = get_config()
        stanza = configs["name"]
        # server_uri = configs["server_uri"]
        # sessionKey = configs["session_key"]
        # userName = "admin"   # make this modular input as application context only.

        """
        wevts = configs["events"].strip()
        if len(wevts) <= 0:
            wevts = ["Objects", "Server"]
        else:
            wevts = wevts.split(":")
            
        patterns = configs["event_types"].strip()
        if len(patterns) <= 0:
            patterns = ["*"]
        else:
            patterns = patterns.split(":")
        """
            
        tout = configs["connection_timeout"].strip()
        timeout = 1 if len(tout) <= 0 else int(tout)

        cdur = configs["collect_duration"].strip()
        duration = 1000 if len(cdur) <= 0 else int(cdur)
        
        conn = configs["connection"]   ## "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"
        if configs.has_key("username"):
            username = configs["username"].strip()
            if len(username)>0:
                password = configs["password"].strip()
                conn = "%s?username=%s&password=%s" % (conn, username, password)
    
        client = Client(conn, timeout=timeout)
        
        try:
            client.connect()
            #root = client.get_root_node()
            #m = node.get_child(root, wevts)
            #measures = []
            #node.collect_measures(measures, wevts, root)
                    
            handler = SubHandler(stanza)
            sub = client.create_subscription(duration, handler)
            h = sub.subscribe_events()
        
            """
            handles = []
            
            for evt in measures:
                try:
                    h = sub.subscribe_events(evt[len(evt)-1])
                    handles.append(h)
                except Exception as ex:
                    logger.warn(ex)
            """    
       
            def signal_handler(signal, frame):
                logger.info('Press Ctrl+C')
                
                if signal in [signal.SIGABRT, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM]:
                    #[sub.unsubscribe(h) for h in handles]
                    sub.unsubscribe(h)
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
            logger.info("---- end of sub opc ua ----")

if __name__ == '__main__':
    logger.info("---- sub opc ua ----")
    try:
        run()
    except Exception as ex:
        logger.critical(ex)

