'''
Created on Jan 14, 2016

@author: btsay
'''
import os
import sys
import xml.dom.minidom

import logging.handlers

LOGGER_FORMAT = '%(asctime)s [%(levelname)s] [%(filename)s] %(message)s'

def create_logger_handler(fd, level, maxBytes=10240000, backupCount=5):
    handler = logging.handlers.RotatingFileHandler(fd, maxBytes=maxBytes, backupCount=backupCount)
    handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    handler.setLevel(level)
    return handler

def setup_logging(app, level=logging.INFO):
    logger = logging.Logger(app)
    try:
        LOG_FILENAME = os.path.join(os.environ.get('SPLUNK_HOME'), 'var','log','splunk','%s.log' % app)
        logger.setLevel(level)
        handler = create_logger_handler(LOG_FILENAME, level)
        logger.addHandler(handler)
    except:
        pass
    return logger

def get_config(config_str):
    config = {}
    try:
        doc = xml.dom.minidom.parseString(config_str.strip())
        server_uri = doc.getElementsByTagName("server_uri")[0]
        session_key = doc.getElementsByTagName("session_key")[0]
        config["server_uri"] = server_uri.childNodes[0].nodeValue
        config["session_key"] = session_key.childNodes[0].nodeValue
        
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    config["name"] = stanza_name

                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data

        if not config:
            raise Exception, "Invalid configuration received from Splunk."

    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return config

def os_specific_sys_exit(sysVal):
    # Borrowed from DB Connect Code.
    if sysVal < 0:
        if os.name == 'nt':
            sysVal += 2**32      
        else:
            sysVal += 2**8 

    sys.exit(sysVal)
    

def format_float(s):
    st = s
    try:
        t = str(s)
        i = t.index('.')+3
        st = float(t[:i])
    except ValueError:
        pass
    
    return st

'''
print format_float('abc')
print format_float('12')
print format_float('12.')
print format_float('12.0')
print format_float('12.01')
print format_float('12.012')
print format_float('12.0123')
print format_float(12.0123)
'''