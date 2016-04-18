import splunk_opcua.utils as utils
logger = utils.setup_logging("opcua")

import sys
sys.path.insert(0, "..")

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import ua, uamethod, Server

# method to be exposed through server

def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y


def run(nodejson, endpoint, namespace, description):

    # now setup our server
    server = Server()
    #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint(endpoint)
    server.set_server_name(description)

    # setup our own namespace
    uri = namespace
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    variables = {}
    
    nodeId = 5
    
    def add_variable(f, vals, nodeId):
        for x in vals:
            k = x if isinstance(x, str) or isinstance(x, unicode) else x.keys()[0]
            #v = f.add_variable("ns=6;i=600%d" % nodeId, k, ua.Variant([], ua.VariantType.Float))
            v = f.add_variable("ns=6;i=600%d" % nodeId, x, ua.Variant([], ua.VariantType.Float))
            # nodeid, browsename, value, [variant type]
            #v = f.add_variable("ns=6;s=%s" % x, x, ua.Variant([], ua.VariantType.Float))
            v.set_writable()
            variables[k] = v
            nodeId = nodeId+1
            
        return nodeId
    
    
    def add_folder(p, pid, val, nodeId):
        for n, v in val.items():
            mf = p.add_folder("ns=%d;i=%d00%d" % (pid, pid, nodeId), n)
            #mf = p.add_folder("ns=%d;s=%s" % (pid, n), n)
            
            if isinstance(v, list) or isinstance(v, tuple):
                nodeId = add_variable(mf, v, nodeId+1)
            else:
                nodeId = add_folder(mf, pid+1, v, nodeId+1)

        return nodeId
    
    # populating our address space
    add_folder(objects, 5, nodejson, nodeId)
                
    
    '''
    myobj = objects.add_object(idx, "MyObject")
    
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    myvar.set_writable()    # Set MyVariable to be writable by clients
    myarrayvar = myobj.add_variable(idx, "myarrayvar", [6.7, 7.9])
    myarrayvar = myobj.add_variable(idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32))
    myprop = myobj.add_property(idx, "myproperty", "I am a property")
    mymethod = myobj.add_method(idx, "mymethod", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    
                
    inargx = ua.Argument()
    inargx.Name = "x"
    inargx.DataType = ua.NodeId(ua.ObjectIds.Int64)
    inargx.ValueRank = -1
    inargx.ArrayDimensions = []
    inargx.Description = ua.LocalizedText("First number x")
    inargy = ua.Argument()
    inargy.Name = "y"
    inargy.DataType = ua.NodeId(ua.ObjectIds.Int64)
    inargy.ValueRank = -1
    inargy.ArrayDimensions = []
    inargy.Description = ua.LocalizedText("Second number y")
    outarg = ua.Argument()
    outarg.Name = "Result"
    outarg.DataType = ua.NodeId(ua.ObjectIds.Int64)
    outarg.ValueRank = -1
    outarg.ArrayDimensions = []
    outarg.Description = ua.LocalizedText("Multiplication result")

    multiply_node = myobj.add_method(idx, "multiply", multiply, [inargx, inargy], [outarg])
    '''
    # starting!
    server.start()
    #print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    
    return server, variables
    
    
import time
import thread
import random
    
def post_run(server, variables):    
    # Define a function for the thread
    def set_value():
        while True:
            for n, v in variables.items():
                r = random.randint(0, 100)
                v.set_value(r, ua.VariantType.UInt32)
            time.sleep(10)
    
    # Create two threads as follows
    try:
        thread.start_new_thread( set_value, () )
    except:
        print "Error: unable to start thread"

    try:
        embed()
    finally:
        server.stop()

'''
if __name__ == "__main__":
    njson = {
             "Backwash Recovery":{
                                  "Recovery Basin 2":[
                                                      "SeamountRecoveryBasin2ORPLevel",
                                                      "SeamountRecoveryBasin2WaterLevel"
                                                      ],
                                  "Recovery Ozone Tower":[
                                                          "SeamountRecoveryOZCTowerDischargeORPLevel",
                                                          "SeamountRecoveryOZCTowerFlow",
                                                          "SeamountRecoveryOZCWaterLevel"
                                                          ],
                                  "Recovery Filter":[
                                                     "SeamountRecoveryFilterFlow"
                                                     ],
                                  "Recovery Basin 1":[
                                                      "SeamountRecoveryBasin1ORPLevel",
                                                      "SeamountRecoveryBasin1WaterLevel"
                                                      ],
                                  "Recovery Protein Skimmer":[
                                                              "SeamountRecoveryPSKDischargeORPLevel",
                                                              "SeamountRecoveryPSKWaterLevel"
                                                              ]
                                  },
             "Deaeration":{
                           "Deaeration Tower":[
                                               "SeamountDeaerationTowerDischargeORPLevel",
                                               "SeamountDeaerationTowerWaterLevel"
                                               ]
                           },
             "Ozonation System":{
                                 "Ozone Tower 2":[
                                                  "SeamountOZCTower2DischargeORPLevel",
                                                  "SeamountOZCTower2Flow",
                                                  "SeamountOZCTower2WaterLevel"
                                                  ],
                                 "Ozone Tower 1":[
                                                  "SeamountOZCTower1DischargeORPLevel",
                                                  "SeamountOZCTower1Flow",
                                                  "SeamountOZCTower1WaterLevel"
                                                  ]
                                 },
             "Foam Fractionation":{
                                   "Protein Skimmer 1":[
                                                        "SeamountPSK1DischargeORPLevel",
                                                        "SeamountPSK1WaterLevel"
                                                        ],
                                   "Protein Skimmer 2":[
                                                        "SeamountPSK2DischargeORPLevel",
                                                        "SeamountPSK2WaterLevel"
                                                        ],
                                   "Protein Skimmer 3":[
                                                        "SeamountPSK3DischargeORPLevel",
                                                        "SeamountPSK3WaterLevel"
                                                        ],
                                   "Protein Skimmer 4":[
                                                        "SeamountPSK4DischargeORPLevel",
                                                        "SeamountPSK4WaterLevel"
                                                        ],
                                   "Protein Skimmer 5":[
                                                        "SeamountPSK5DischargeORPLevel",
                                                        "SeamountPSK5WaterLevel"
                                                        ]
                                   },
             "Sand Filtration System":{
                                       "Filter 7/8":[
                                                     "SeamountFilter78Flow"
                                                     ],
                                       "Filter 5/6":[
                                                     "SeamountFilter56Flow"
                                                     ],
                                       "Filter 9/10":[
                                                      "SeamountFilter910Flow"
                                                      ],
                                       "Filter 3/4":[
                                                     "SeamountFilter34Flow"
                                                     ],
                                       "Filter 1/2":[
                                                     "SeamountFilter12Flow"
                                                     ]
                                       }
             }
    
    endpoint = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
    namespace = "http://opcua.splunk.com"
    description = "FreeOpcUa Example Server"
    
    server, vars = run(njson, endpoint, namespace, description)
    post_run(server, vars)
    
'''