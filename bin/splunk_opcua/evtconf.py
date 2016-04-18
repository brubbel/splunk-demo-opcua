
defaults = {
"random_select" : {
    "description" : "randomly generate values with equal probability or a ratio",
    "python" : "splunk_opcua.evtsim.random_select",
    "ratio" : "*",
    "seed" : "123"
    },
"number_range_select" : {
    "description" : "generate values with equal probability or a ratio within a range",
    "python" : "splunk_opcua.evtsim.number_range_select",
    "range" : "1:100",
    "ratio" : "[1-20]:5,[21-40]:2,[41-100]:1"
    },

"number_range_rotate" : {
    "description" : "generate values with equal probability or a ratio within a range and rotate while reaching the end.",
    "python" : "splunk_opcua.evtsim.number_range_rotate",
    "range" : "1:100",
    "ratio" : "[1-20]:5,[21-40]:2,[41-100]:1"
    },
"random_number_range_select" : {
    "description" : "randomly generate values with equal probability or a ratio within a range",
    "python" : "splunk_opcua.evtsim.random_number_range_select",
    "range" : "1:100",
    "ratio" : "[1-20]:5,[21-40]:2,[41-100]:1"
    },
"float_range_rotate" : {
    "description" : "generate values with equal probability or a ratio within a float range and rotate while reaching the end.",
    "python" : "splunk_opcua.evtsim.float_range_rotate",
    "range" : "0.1:1.2"
    },
"random_float_range_select" : {
    "description" : "randomly generate values with equal probability or a ratio within a float range",
    "python" : "splunk_opcua.evtsim.random_float_range_select",
    "range" : "0.7:1.5",
    "ratio" : "[0.7-1.2]:5,[1.3-]:2"
    },
"random_select_from_file" : {
    "description" : "randomly generate values from a file with equal probability or a ratio",
    "python" : "splunk_opcua.evtsim.random_select_from_file",
    "ratio" : "*",
    "seed" : "123",
    "file" : ""
    }, 
"composite_field" : {
    "description" : "compose a list fields",
    "python" : "splunk_opcua.evtsim.composite_field",
    "value" : ""
    }  
}                  

import os
import json
import ta_opcua

def get_locals():
    evts = os.path.join(ta_opcua.data_dir(), "events.json")
    with open(evts) as json_file:
        json_data = json.load(json_file)
        json_file.close()
        
    return json_data

def get_defaults():
    return defaults

    
    