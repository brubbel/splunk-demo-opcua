import os
import json
import splunk_opcua.evtconf as evtconf
import ta_opcua
def get_locals():
    evts = os.path.join(ta_opcua.data_dir(), "metrics2.json")
    with open(evts) as json_file:
        json_data = json.load(json_file)
        json_file.close()
        
    return json_data

def get_defaults():
    return evtconf.get_defaults()

