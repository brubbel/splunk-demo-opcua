import os.path as path
import os
import sys

class RequireError(NameError):
    pass

def require(namespace):
    current_app = path.abspath(path.join(path.dirname(path.realpath(__file__)), os.pardir, os.pardir))
    if not os.environ.has_key("SPLUNK_HOME"):
        os.environ["SPLUNK_HOME"] = path.abspath(path.join(current_app, os.pardir, os.pardir, os.pardir))
        
    nshome = path.abspath(path.join(os.environ["SPLUNK_HOME"], "etc", "apps", namespace))
    if not os.path.exists(nshome):
        raise RequireError("splunk app : %s is required by current app!" % namespace)
    
    sys.path.append(path.abspath(path.join(nshome, "bin")))


def data_dir():
    p = os.path.realpath(__file__)
    return os.path.abspath(os.path.join(p, os.pardir, os.pardir, os.pardir, "data"))


def get_locals(pkg):
    return pkg.get_locals()

def get_defaults(pkg):
    return pkg.get_defaults()

def get_configs(pkg):
    configs = get_defaults(pkg)
    configs.update(get_locals(pkg))
    return configs

def GET(f, pkg, get_configs=get_configs):
    configs = get_configs(pkg)
    c = configs.get(f)
    assert c, "object [%s] must exist." % f
    k = None
    while c.has_key("extend"):
        if c["extend"] != k:
            x = configs[c["extend"]];
            k = c["extend"]
            x.update(c)
            c = x
        else:
            break
        
    return c

def GET_ALL(pkg):
    all = {}
    for n in get_locals(pkg):
        all[n] = GET(n, pkg)
        
    return all


import importlib
'''
from entity of the configuration to invoke the generator object.
'''
def invoke_object(conf):
    p = conf["python"]
    c = p.split(".")
    pkg = ".".join(c[0:len(c)-1])
    o = c[len(c)-1]
    module = importlib.import_module(pkg)
    f = getattr(module, o)
    return f(conf)


"""
# Usage examples:
    
import fields
import timers

print GET("ip", fields)
print GET("my_raw_time", timers)
print GET_ALL(fields)
"""

