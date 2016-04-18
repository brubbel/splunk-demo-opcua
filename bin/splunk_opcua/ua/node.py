import fnmatch
from opcua.ua import object_ids
from GenericCache.GenericCache import GenericCache
from GenericCache.decorators import cached

cache = GenericCache()


def pattern_match(name, p):
    mp = p.split("&")
    for m in mp:
        if m.startswith("~"):
            return not fnmatch.fnmatch(name, m[1:])
        elif fnmatch.fnmatch(name, m):
            return True
        
    return False

@cached(cache)
def get_event_type(evt_id):
    for n, v in object_ids.ObjectIds.__dict__.items():
        if str(v) == str(evt_id):
            return str(n)
    
    return str(evt_id)


#@cached(cache)
def collect_measures(measures, pats, n, ns = [], l=0):
    ll = len(pats)
    
    m = ns + [n]
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

def get_child(node, ns):
    c = None
    try:
        c = node.get_child(ns)
    except:
        for x in node.get_children():
            if x.get_browse_name().Name == ns[0]:
                if len(ns)>1:
                    c = get_child(x, ns[1:])
                else:
                    c = x
                break
    return c
    


