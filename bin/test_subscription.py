import fnmatch
from opcua import Client

def pattern_match(name, p):
    mp = p.split("&")
    for m in mp:
        if m.startswith("~"):
            return not fnmatch.fnmatch(name, m[1:])
        elif fnmatch.fnmatch(name, m):
            return True
        
    return False


def collect_measures(measures, pats, n, ns = [], l=0):
    ll = len(pats)
    b = n.get_browse_name()
    
    m = ns + [b.Name]
    c = n.get_children()

    # leaf while there is no sub nodes.
    if len(c)<=0:
        try:
            measures.append(m[1:])
        except Exception as ex:
            print ex
    else:
        for a in c:
            if l>=ll or pattern_match(a.get_browse_name().Name, pats[l]): 
                collect_measures(measures, pats, a, ns=m, l=l+1)


x = dict()
x["name"] = "test"

#    configs["connection"] = "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"
x["connection"] = "opc.tcp://10.1.10.211:53530/OPCUA/SimulationServer"

x["connection_timeout"] = "30"
x["measures"] = "O*:M*:M*:M*Alarm:~En*&H*&E*"
x["separator"] = "|"

y = dict()
y["name"] = "test"

#    configs["connection"] = "opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320"
y["connection"] = "opc.tcp://192.168.77.197:9966"

y["connection_timeout"] = "30"
y["measures"] = "O*:~Serv*"
y["separator"] = "|"

def get_configs():
    return y

import time
def run():
    configs = get_configs()
    
    patterns = configs["measures"].split(":")
    tout = configs["connection_timeout"].strip()
    timeout = 1 if len(tout) <= 0 else int(tout)

    client = Client(configs["connection"], timeout=timeout)
    
    try:
        client.connect()
        measures = []
        root = client.get_root_node()
        collect_measures(measures, patterns, root)
        
        for x in root.get_children():
            print x.get_browse_name().Name
            
        for m in measures:
            print m
            
        time.sleep(30)
    except Exception as ex:
        print ex
    finally:
        client.disconnect()

if __name__ == '__main__':
    try:
        run()
    except Exception as ex:
        print ex

