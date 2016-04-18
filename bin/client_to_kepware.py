import sys
sys.path.insert(0, "..")
import logging
import time

from opcua import Client
#from opcua import uaprotocol as ua


class SubHandler(object):

    """
    Client to subscription. It will receive events from server
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)



"""Test whether FILENAME matches PATTERN.

Patterns are Unix shell style:

*       matches everything
?       matches any single character
[seq]   matches any character in seq
[!seq]  matches any char not in seq

An initial period in FILENAME is not special.
Both FILENAME and PATTERN are first case-normalized
if the operating system requires it.
If you don't want this, use fnmatchcase(FILENAME, PATTERN).
"""

import fnmatch
lst = ['this','is','just','a','test']
filtered = fnmatch.filter(lst, 'th?s')

#fnmatch.fnmatch(name, pat)


def match_nodes(pnode, pattern):
    nodes = [n.get_browse_name().Name for n in pnode.get_children()]
    if len(nodes) > 0:
        return fnmatch.filter(nodes, pattern)
    else:
        return None



def get_children(n, ns = []):
    b = n.get_browse_name()
    
    m = ns + [b.Name]
    
    c = n.get_children()
    if len(c)<=0:
        try:
            obj = "/".join(m)
            data = n.get_data_value()
            
            val_type = data.Value.VariantType.name
            val = data.Value.Value
            
            sc =  data.StatusCode.name
            dt = str(data.SourceTimestamp)
            
            str_data_types = ["String", "DateTime", "LocalizedText", "Variant", "ByteString", "XmlElement", "QualifiedName"]
            if isinstance(val,list):
                for v in val:
                    if val_type in str_data_types:
                        dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=\"%s\"" % (dt,obj,sc,val_type,v)
                    else:
                        dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=%s" % (dt,obj,sc,val_type,v)
            else:
                if val_type in str_data_types:
                    dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=\"%s\"" % (dt,obj,sc,val_type,val)
                else:
                    dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=%s" % (dt,obj,sc,val_type,val)
                
            print dv
        except:
            pass

    else:        
        for a in c:
            print_children(a, m)



if __name__ == "__main__":
    csvf = open("opcua.csv", "w+")
    kvf = open("opcua.kv", "w+")
    csvf.write ("_time,data_object,status,data_type,value\n")
    

    def print_children(n, ns = []):
        b = n.get_browse_name()
        
        m = ns + [b.Name]
        
        c = n.get_children()
        if len(c)<=0:
            try:
                obj = "/".join(m)
                data = n.get_data_value()
                
                val_type = data.Value.VariantType.name
                val = data.Value.Value
                
                sc =  data.StatusCode.name
                dt = str(data.SourceTimestamp)
                
                str_data_types = ["String", "DateTime", "LocalizedText", "Variant", "ByteString", "XmlElement", "QualifiedName"]
                if isinstance(val,list):
                    for v in val:
                        if val_type in str_data_types:
                            dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=\"%s\"" % (dt,obj,sc,val_type,v)
                        else:
                            dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=%s" % (dt,obj,sc,val_type,v)
                else:
                    if val_type in str_data_types:
                        dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=\"%s\"" % (dt,obj,sc,val_type,val)
                    else:
                        dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=%s" % (dt,obj,sc,val_type,val)
                    
                print dv
            except:
                pass

        else:        
            for a in c:
                print_children(a, m)


    
    def dump_children(n, ns = []):
        b = n.get_browse_name()
        
        m = ns + [b.Name]
        
        c = n.get_children()
        if len(c)<=0:
            try:
                obj = "/".join(m)
                data = n.get_data_value()
                
                val_type = data.Value.VariantType.name
                val = data.Value.Value
                
                sc =  data.StatusCode.name
                dt = str(data.SourceTimestamp)
                
                str_data_types = ["String", "DateTime", "LocalizedText", "Variant", "ByteString", "XmlElement", "QualifiedName"]
                if isinstance(val,list):
                    for v in val:
                        if val_type in str_data_types:
                            cdv = "\"%s\",\"%s\",%s,%s,\"%s\"" % (dt,obj,sc,val_type,v)
                            dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=\"%s\"" % (dt,obj,sc,val_type,v)
                        else:
                            cdv = "\"%s\",\"%s\",%s,%s,%s" % (dt,obj,sc,val_type,v)
                            dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=%s" % (dt,obj,sc,val_type,v)
                else:
                    if val_type in str_data_types:
                        cdv = "\"%s\",\"%s\",%s,%s,\"%s\"" % (dt,obj,sc,val_type,val)
                        dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=\"%s\"" % (dt,obj,sc,val_type,val)
                    else:
                        cdv = "\"%s\",\"%s\",%s,%s,%s" % (dt,obj,sc,val_type,val)
                        dv = "_time=\"%s\" data_object=\"%s\" status=%s data_type=%s value=%s" % (dt,obj,sc,val_type,val)
                    
                
                # print("%s = %s\n" % (ns, n.get_data_value()))
                kvf.write("%s\n" % dv)
                csvf.write("%s\n" % cdv)
            except:
                pass

        else:        
            for a in c:
                dump_children(a, m)
            
        
    
    #from IPython import embed
    logging.basicConfig(level=logging.WARN)
    #client = Client("opc.tcp://192.168.56.100:49320/OPCUA/SimulationServer/")
    #client = Client("opc.tcp://192.168.56.100:4841/OPCUA/SimulationServer/")
    #client = Client("opc.tcp://olivier:olivierpass@localhost:53530/OPCUA/SimulationServer/")
    client = Client("opc.tcp://ec2-54-190-162-94.us-west-2.compute.amazonaws.com:49320")
    
    try:
        client.connect()
        root = client.get_root_node()
        objnode = client.get_objects_node()
        
        pats = "W*:T*".split(":")
        
        
        for p in pats:
            
            nodes = match_nodes(objnode, p)
            
            
            
            for n in nodes:
                xn = match_nodes(n, p)




        #dump_children(objnode)
        
        a = objnode.get_child(["Windfarm_01", "Turbine_01", "Power"])
        print a.get_browse_name()
        print a.get_data_type()
        print a.get_data_value()
        print a.get_value()
        print a.get_node_class()
        
        b = objnode.get_child(["Windfarm_01", "Turbine_01"])
        
        print_children(b, ["Windfarm_01"])
        
        c = b.get_children()
        
        
        
        # b = client.get_node("ns=2;s=Windfarm_01.Turbine_01.Power")
        
        #dump_children(a, ["Windfarm_01", "Turbine_01"])
        
        
        # get_children(objnode)
        
        
        
        # get_children(root)
        
        """
        objects = client.get_objects_node()

        objdict = {}

        for n in objects.get_children():
            objdict[n.get_browse_name()] = [n.get_browse_name()]
            
            
            for x in n.get_children():
                print x.get_node_class()
                y = x.get_children()
                if len(y) > 0 :
                    for z in y:
                        print z.get_node_class()
                        print z.get_value()
                
                try:
                    print x.get_values()
                except:
                    print x.get_browse_name()
            try:
                print "%s %s" % (n.nodeid, n.get_node_class())
            except Exception as ex:
                print ex
                print n.get_browse_name()
                


        alarms = client.get_node("ns=2;s=_CustomAlarms")
        print alarms.get_browse_name()
        print alarms.get_description()
        print alarms.get_properties()
        #print alarms.get_value()
        #print alarms.get_data_type()
        #print alarms.get_data_value()
        
        #print("alarms are: {} with value {} ".format(alarms, alarms.get_value()))
        idf = client.get_node("ns=2;s=_IDF_for_Splunk")
        print idf.get_browse_name()
        print idf.get_description()
        print idf.get_properties()
        
        #print("IDF is: {} with value {} ".format(idf, idf.get_value()))
        

        
        tag1 = client.get_node("ns=2;s=Channel1.Device1.Tag1")
        print("tag1 is: {} with value {} ".format(tag1, tag1.get_value()))
        tag2 = client.get_node("ns=2;s=Channel1.Device1.Tag2")
        print("tag2 is: {} with value {} ".format(tag2, tag2.get_value()))
        """
        
        # handler = SubHandler()
        # sub = client.create_subscription(500, handler)
        #handle = sub.subscribe_data_change(alarms)
        #print handle
        
        #handle = sub.subscribe_data_change(idf)
        
        #print handler

        #from IPython import embed
        #embed()

        
        #sub.unsubscribe(handle)
        # sub.delete()
    finally:
        client.disconnect()
