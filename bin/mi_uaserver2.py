'''
Created on Jan 12, 2016

@author: btsay
'''

import splunk_opcua.utils as utils
logger = utils.setup_logging("opcua")

import sys

from splunk_opcua.ua import server
from opcua import ua


SCHEME = """
<scheme>
    <title>UA Simulator Server II</title>
    <description>OPC UA Server Simulator II.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>

    <endpoint>
        <args>

            <arg name="serverpath">
                <title>UA Server path</title>
                <description>OPC UA server path.</description>
            </arg>

            <arg name="namespace">
                <title>UA Service Namespace</title>
                <description>OPC UA service Namespace.</description>
            </arg>

            <arg name="description">
                <title>Description</title>
                <description>The server description of the UA Server.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="serverport">
                <title>UA Server port</title>
                <description>UA Server Port.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="nodefile">
                <title>Node Structure</title>
                <description> Node Structure JSON file.</description>
            </arg>

            <arg name="username">
                <title>OPC Server Login User Account</title>
                <description> Login User Account to access UA server.</description>
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
                <title>UA Server Connection Timeout</title>
                <description> connection Timeout to access UA server.</description>
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

import os, uaserver, csv
import signal, json
import time
import evtconf2
import ta_opcua

running = True

def random_events():
    evtgen = {}
    for f in evtconf2.get_locals().keys():
        conf = ta_opcua.GET(f, evtconf2)
        evtgen[f] = ta_opcua.invoke_object(conf)
    
    return evtgen

def post_run(server, variables, interval):    
    try:
        evts = random_events()
        ekeys = evts.keys()
        while running:
            for k in ekeys:
                if variables.has_key(k):
                    fv = evts[k].next()
                    # print k, fv
                    variables[k].set_value(float('{:10.3f}'.format(float(fv))), ua.VariantType.Float)
                        
            time.sleep(interval)
    finally:
        server.stop()    

def run():

    logger.info("Start running.........")
    
    confs = get_config()
    serverpath = confs["serverpath"]
    description = confs["description"]
    stanza = confs["name"]
    interval = confs["interval"]
    serverport = confs["serverport"]
    nodefile = confs["nodefile"]
    namespace = confs["namespace"]
    interval = confs["interval"]
    endpoint = "opc.tcp://0.0.0.0:%s%s" % (serverport, serverpath)
        
    logger.info("Data File is loaded.")
    
    nf = os.path.join(uaserver.data_dir(), nodefile)
    with open(nf, 'rU') as fd:
        nodejson = json.load(fd)
        fd.close()
        
    logger.info("Address space is loaded.")
        
    s, v = server.run(nodejson, endpoint, namespace, description)

    logger.info("UA server is running...")
            
    post_run(s, v, int(interval))

if __name__ == '__main__':
    
    def handler(signum, frame):
        if signum in [signal.SIGINT, signal.SIGABRT, signal.SIGTERM]:
            running = False
            exit(0)
            
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGABRT, handler)
    signal.signal(signal.SIGTERM, handler)

    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            try:    
                do_scheme()
            except Exception as ex:
                logger.critical(ex)
        elif sys.argv[1] == "--validate-arguments":
            validate_arguments()
        elif sys.argv[1] == "--test":
            test()
        else:
            usage()
    else:
        run()
        
