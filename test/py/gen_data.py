'''
Created on Mar 22, 2016

@author: btsay
'''

import os 
from xml.etree import ElementTree
import uaserver as ua

def gen():
    data = os.path.join(ua.data_dir(), "data.xml")
    d = {}
    with open(data, 'rU') as data_file:
        tree = ElementTree.parse(data_file)    
        data_file.close()


    print "Timestamp,Source,Asset,Metric,Value,Unit"
    for node in tree.iter():
        for n in node:
            for nn in n:
                if nn.tag=="data":
                    c = convert(nn.text[27:])
                    if c.has_key("asset"):
                        print "%s,%s,%s,%s,%s,%s" % (c["collect_time"], "OPC", c["asset"], c["metric"], c["value"], c["unit"])


def convert(d):
    z = {}
    for x in d.split(","):
        y = x.split("=")
        z[trim(y[0].strip())] = trim(y[1].strip())
        
    return z
        
        
def trim(z):
    d = []
    dd = False
    for x in z.strip():
        if x not in ['\t', '\n']:
            dd = True
            d.append(x)
        else:
            if dd:
                d.append(" ")
                dd = False
        
    return ''.join(d)
        
        


gen()


