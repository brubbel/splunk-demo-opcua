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
import datetime
from collections import OrderedDict as odict

from splunk_opcua import mi
import mi_uaserver2 as mi_ua

SCHEME = """
<scheme>
    <title>IoT Events Generation</title>
    <description>Generate all events IoT Demo project needs.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>

    <endpoint>
        <args>

            <arg name="description">
                <title>Descrption</title>
                <description>Description for this event generation.</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>

            <arg name="assets">
                <title>Assets Configuration</title>
                <description> The configuration of assets and their metrics.</description>
            </arg>

            <arg name="metrics">
                <title>Metrics Configuration</title>
                <description> The configuration of metrics and how to generate data.</description>
            </arg>

            <arg name="conditions">
                <title>Alerts and Conditions</title>
                <description>The configuration of conditions and generation of alerts.</description>
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

'''
Asset    Healthscore (0-100)
Holding basin    N/A
PSK Pump     (Deviation from optimal flow)*1/3 + (Deviation from optimal pressure)*1/3 + (Downtime hours / Optimal downtime hours)*1/3 
Protein Skimmer 1 - 5     (Deviation from optimal flow)*1/2 + (Downtime hours / Optimal downtime hours)*1/2 
PSK recirculation pump     (Deviation from optimal flow)*1/3 + (Deviation from optimal pressure)*1/3 + (Downtime hours / Optimal downtime hours)*1/3 
Sand Filter Pump 1 - 5     (Deviation from optimal flow)*1/3 + (Deviation from optimal pressure)*1/3 + (Downtime hours / Optimal downtime hours)*1/3 
Sand Filter 1/2 - 9/10     (Deviation from optimal flow)*1/2 + (Downtime hours / Optimal downtime hours)*1/2 
Denitrification Filter Valve      (Deviation from optimal pressure)*1/2 + (Downtime hours / Optimal downtime hours)*1/2 
Denitrification Filter     (Deviation from optimal flow)*1/2 + (Downtime hours / Optimal downtime hours)*1/2 
Ozone Tower Valve      (Deviation from optimal pressure)*1/2 + (Downtime hours / Optimal downtime hours)*1/2 
Ozone Tower 1 - 2     N/A 
Ozone Tower Recirculation Pump     (Deviation from optimal flow)*1/3 + (Deviation from optimal pressure)*1/3 + (Downtime hours / Optimal downtime hours)*1/3 
Deaeration Tower     N/A 
Output Pump 1 - 5     (Deviation from optimal flow)*1/3 + (Deviation from optimal pressure)*1/3 + (Downtime hours / Optimal downtime hours)*1/3 
Water Quality Sensor     N/A 
'''


def health_score(o, j_asset, j_downtime):
    asset = o["Asset"]
    score = dict()
    score["PSK Pump"] = (40, 45)
    score["Protein Skimmer 1"] = (35, 40)
    score["Protein Skimmer 2"] = (40, 45)
    score["Protein Skimmer 3"] = (20, 25)
    score["Protein Skimmer 4"] = (15, 20)
    score["Protein Skimmer 5"] = (60, 65)
    score["PSK Recirculation Pump"] = (70, 75)
    score["Sand Filter Pump 1"] = (90, 95)
    score["Sand Filter Pump 2"] = (85, 90)
    score["Sand Filter Pump 3"] = (40, 45)
    score["Sand Filter Pump 4"] = (45, 50)
    score["Sand Filter Pump 5"] = (30, 35)
    score["Sand Filter 1/2"] = (50, 55)
    score["Sand Filter 3/4"] = (25, 30)
    score["Sand Filter 5/6"] = (35, 40)
    score["Sand Filter 7/8"] = (30, 35)
    score["Sand Filter 9/10"] = (60, 65)
    score["Denitrification Filter Valve"] = (70, 75)
    score["Denitrification Filter"] = (75, 80)
    score["Ozone Tower Valve"] = (65, 70)
    score["Ozone Tower Recirculation Pump"] = (50, 55)
    score["Output Pump 1"] = (65, 70)
    score["Output Pump 2"] = (45, 50)
    score["Output Pump 3"] = (70, 75)
    score["Output Pump 4"] = (70, 75)
    score["Output Pump 5"] = (85, 90)
    
    r = 0
    if score.has_key(asset):
        r = random.randrange(score[asset][0], score[asset][1])

    '''
    r = 0
    if asset in ["PSK Pump", "PSK Recirculation Pump", "Sand Filter Pump 1", "Sand Filter Pump 2",
                 "Sand Filter Pump 3", "Sand Filter Pump 4", "Sand Filter Pump 5", "Ozone Tower Recirculation Pump",
                 "Output Pump 1", "Output Pump 2", "Output Pump 3", "Output Pump 4", "Output Pump 5",
                 "Protein Skimmer 1", "Protein Skimmer 2", "Protein Skimmer 3", "Protein Skimmer 4",
                 "Protein Skimmer 5", "Sand Filter 1/2", "Sand Filter 3/4", "Sand Filter 5/6",
                 "Sand Filter 7/8", "Sand Filter 9/10", "Denitrification Filter",                 
                 "Denitrification Filter Valve", "Ozone Tower Valve"
                 ]:
        r = random.randrange(20, 101)
    '''
    o["Healthscore"] = dict(value = "%s" % r if r > 0 else "N/A", unit = "N/A")
    

'''
def health_score(o, j_asset, j_downtime):
    asset = o["Asset"]
    
    r = 0.0
    
    r_downtime = 0
    if j_downtime.has_key(asset):
        r_downtime = float(j_downtime[asset]["downtime"])/float(j_downtime[asset]["optimum"])

    # PSK recirculation pump
    if asset in ["PSK Pump", "PSK Recirculation Pump", "Sand Filter Pump 1", "Sand Filter Pump 2",
                 "Sand Filter Pump 3", "Sand Filter Pump 4", "Sand Filter Pump 5", "Ozone Tower Recirculation Pump",
                 "Output Pump 1", "Output Pump 2", "Output Pump 3", "Output Pump 4", "Output Pump 5"]:
        r_flow = 0.0
        r_pressure = 0.0
        
        if o.has_key("Pressure"):
            pressure = float(o["Pressure"]["value"])
            optimum = float(o["Pressure"]["optimum"])
            r_pressure = abs(optimum-pressure)/optimum
        
        if o.has_key("Flow"):
            flow = float(o["Flow"]["value"])
            optimum = float(o["Flow"]["optimum"])
            r_flow = abs(optimum-flow)/optimum
                
        r = 33.3 * (r_downtime + r_flow + r_pressure)
        
    elif asset in ["Protein Skimmer 1", "Protein Skimmer 2", "Protein Skimmer 3", "Protein Skimmer 4",
                 "Protein Skimmer 5", "Sand Filter 1/2", "Sand Filter 3/4", "Sand Filter 5/6",
                 "Sand Filter 7/8", "Sand Filter 9/10", "Denitrification Filter"]:
        
        r_flow = 0
        
        if o.has_key("Flow"):
            flow = float(o["Flow"]["value"])
            optimum = float(o["Flow"]["optimum"])
            r_flow = abs(optimum-flow)/optimum
                
        r = 50.0 * (r_flow + r_downtime)
        
    elif asset in ["Denitrification Filter Valve", "Ozone Tower Valve"]:
        r_pressure = 0
        
        if o.has_key("Pressure"):
            pressure = float(o["Pressure"]["value"])
            optimum = float(o["Pressure"]["optimum"])
            r_pressure = abs(optimum-pressure)/optimum
                
        r = 50.0 * (r_downtime + r_pressure)
        
    o["Healthscore"] = dict(value = "%s" % r if r > 0.0 else "N/A", unit = "N/A")
   
'''   
    
def compare(val, v):
    op = v[0]
    ov = float(v[1:].strip())
    return (op == "<" and val < float(ov)) or (op == ">" and val > float(ov)) or False
    
def match_condition(o, c):
    r_c = None
    try:
        metric = o[c["metric"]]
        val = float(metric["value"])
        if metric.has_key("optimum"):
            optimum = float(metric["optimum"])
            val = 100 * abs(val-optimum)/optimum
        
        for n, v in c["conditions"].items():
            if compare(val, v):
                r_c = n
                break

    except:
        pass
        
    return "Alarm", r_c
    
import csv, uaserver, random

def gen_opc_alert():
    f_alert = os.path.join(ua.data_dir(), "EventLog_2016_01.dat")

    d = []
    with open(f_alert, 'rU') as fd:
        odr = uaserver.OrderedDictReader(fd, dialect=csv.excel_tab)
        data = [o for o in odr]
        
        fd.close()
    
    dl = len(data)
    
    cc = random.randrange(10, 30)
    for c in range(cc):
        d.append(data[random.randrange(0, dl)])
    
    return d


    
def gen_alert(o, j_conditions, j_metrics):
    alerts = []
    
    for n, vc in j_conditions.items():
        m = vc["metric"]
        if o.has_key(m):
            t, u = match_condition(o, vc)
            if u:
                x = odict()
                x["Asset"] = o["Asset"]
                x["DateTime"] = o["DateTime"]
                x["Source"] = vc["source"]
                x["Alert_Event"] = n
                x["Metric"] = m
                x["Value"] = o[m]["value"]
                x["Unit"] = o[m]["unit"]
                    
                x["Type"] = t
                x["Urgency"] = u
                
                alerts.append(x) 
    
    return alerts

def convert_data(o):
    evt = odict()
    for n, v in o.items():
        if not isinstance(v, dict):
            evt[n] = v
        else:
            evt[n] = v["value"]
            
    return evt
    
def convert_opc_alert(o):
    evt = odict()
    evt["Source"] = "OPC"
    evt["Type"] = o["Type"]
    evt["Asset"] = o["Name"]
    evt["Alert_Event"] = o["Event"]
    evt["Metric"] = "N/A"
    evt["Unit"] = "N/A"
    evt["Urgency"] = "N/A"

    return evt

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
        all_events = []
        
        configs = get_config()
        stanza = configs["name"]
        c_asset = configs["assets"]
        c_metric = configs["metrics"]
        c_condition = configs["conditions"]
        f_asset = os.path.join(ua.data_dir(), c_asset)
        f_metric = os.path.join(ua.data_dir(), c_metric)
        f_condition = os.path.join(ua.data_dir(), c_condition)
        f_downtime = os.path.join(ua.data_dir(), "downtime.json")

        with open(f_metric, 'rU') as fp_m:
            j_metric = json.load(fp_m)
            fp_m.close()
            
        with open(f_condition, 'rU') as fp_c:
            j_condition = json.load(fp_c)
            fp_c.close()

        with open(f_downtime, 'rU') as fp_d:
            j_downtime = json.load(fp_d)
            fp_d.close()
        
        evts = mi_ua.random_events()
        t = datetime.datetime.today()

        opc_alerts = gen_opc_alert()
        
        for opc in opc_alerts:
            all_events.append(convert_opc_alert(opc))
        
        with open(f_asset, 'rU') as fp_a:
            j_asset = json.load(fp_a)
            fp_a.close()
            
            for a, v in j_asset.items():
                o = odict()
                o["DateTime"] = t
                o["Asset"] = a
                o["Type"] = "Data"
                collected = False
                for m in v["metrics"]:
                    if evts.has_key(m):
                        collected = True
                        fv = evts[m].next()
                        nm = j_metric[m]["metric"]
                        o[nm] = dict(measure=m, unit=j_metric[m]["unit"], optimum=j_metric[m]["optimum"], value=fv)
                        
                # has collected data for this asset.
                if collected:
                    health_score(o, j_asset, j_downtime)
                    t = o["DateTime"]
                    
                    all_events.append(convert_data(o))
                    
                    alerts = gen_alert(o, j_condition, j_metric)
                    
                    for alert in alerts:
                        all_events.append(convert_data(alert))

                    '''
                    opc_alerts = gen_opc_alert()
                    for opc in opc_alerts:
                        print_alert(stanza, t, opc, sys.stdout)
                    '''
    
        mi.init_stream(sys.stdout)

        random.shuffle(all_events)
        for evt in all_events:
            mi.print_kv_event(stanza, t, evt, sys.stdout)
            
        mi.fini_stream(sys.stdout)


if __name__ == '__main__':
    logger.info("---- opc ua ----")
    try:
        run()
    except Exception as ex:
        logger.critical(ex)




