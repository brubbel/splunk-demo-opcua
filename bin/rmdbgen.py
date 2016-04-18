import csv
import json
import uaserver as ua
import os

# script to generate metrics.json
def gen_metric_dict():
    metrics = os.path.join(ua.data_dir(), "metrics.csv")
    d = {}
    with open(metrics, 'rU') as data_file:    
        data = csv.DictReader(data_file)
        '''
        "short": "Pressure",
        "datatype": "float",
        "extend": "random_float_range_select",
        "range": "30:32"

        '''
        for x in data:
            m = x["Metric (long name)"]
            d[m] = {}
            d[m]["unit"] = x["Unit"]
            d[m]["metric"] = x["Metric (short name)"]
            d[m]["asset"] = x["Asset"]
            d[m]["extend"] = "random_float_range_select"
            d[m]["range"] = x["Data range"].replace("-", ":")
        data_file.close()

    jmetrics = os.path.join(ua.data_dir(), "metrics.json")
    with open(jmetrics, 'w') as mfp:
        json.dump(d, mfp)
        mfp.close()
            
    print d                    
    return d


#gen_metric_dict()


import os
import json
import ta_opcua
import splunk_opcua.evtconf as evtconf   
import mi_uaserver as m_ua
import uaserver
import datetime    


def get_locals():
    evts = os.path.join(ta_opcua.data_dir(), "metrics.json")
    with open(evts) as json_file:
        json_data = json.load(json_file)
        json_file.close()
        
    return json_data


def get_defaults():
    return evtconf.defaults
    
# script to generate opc five years' data
def gen_opc_data(startdate, duration):
    # data from data file, rotate it.
    cf = os.path.join(uaserver.data_dir(), "DataLog_2016_01.dat")
    
    with open(cf, 'rU') as fd:
        odr = uaserver.OrderedDictReader(fd, dialect=csv.excel_tab)
        data = [o for o in odr]
        datach = uaserver.DataChannel(data, count=1)
        fd.close()

    mf = os.path.join(uaserver.data_dir(), "metrics.json")
    with open(mf, 'rU') as fd:
        metrics = json.load(fd)
        fd.close()
    
    def mtimes():
        enddate = startdate
        while enddate < datetime.datetime.today():
            yield enddate
            enddate = enddate+datetime.timedelta(minutes = duration)
    
    evts = m_ua.random_events()
    ekeys = evts.keys()
    
    mf = os.path.join(uaserver.data_dir(), "measurements.csv")
    num = 1
    with open(mf, 'w') as fd:
        fd.write("mid,measure_time,measure,asset,metric,value,unit\n")
        for t in mtimes():
            for k in ekeys:
                fv = evts[k].next()
                if metrics.has_key(k):
                    fd.write("%d,%s,%s,%s,%s,%s,%s\n" % (num, t, k, metrics[k]["asset"], metrics[k]["metric"], fv, metrics[k]["unit"]))
                    num=num+1
            data = datach.next()
            for d in data:
                for n, v in d.items():
                    if metrics.has_key(n):
                        fd.write("%d,%s,%s,%s,%s,%s,%s\n" % (num, t, n, metrics[n]["asset"], metrics[n]["metric"], v, metrics[n]["unit"]))
                        num=num+1
        fd.close()

# generate 5 years' meansured data.
startdate = datetime.datetime(2011, 1, 1, 0, 0, 0)
duration = 15
                       
gen_opc_data(startdate, duration)
