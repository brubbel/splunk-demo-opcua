import time
import xml.sax.saxutils
current_milliseconds = lambda: int(round(time.time() * 1000))

# prints XML error data to be consumed by Splunk
def print_error(s, out):
    msg = "<error><message>%s</message></error>" % xml.sax.saxutils.escape(s)
    out.write(msg)

def init_stream(out):
    msg = "<stream>"
    out.write(msg)
    

def fini_stream(out):
    msg = "</stream>"
    out.write(msg)


"""
<stream>
  <event stanza="my_config://aaa">
    <time>1330717125</time>
    <data>type=CCC</data>
  </event>
  <event stanza="my_config://bbb">
    <time>1330717125</time>
    <data>type=DDD</data>
  </event>
 . . .
</stream>

<stream>
  <event>
    <time>1370031029</time>
    <data>event_status="(0)The operation completed successfully."</data>
  </event>
  <event>
    <time>1370031031</time>
    <data>event_status="(0)The operation completed successfully."</data>
  </event>
</stream>

"""

def send_data(stanza, t, buf, out):
    _t = xml.sax.saxutils.escape(str(t))
    out.write("<event stanza=\"%s\"><time>" % stanza)
    out.write(_t)
    out.write("</time>\n<data>")
    out.write("%s %s" % (_t, xml.sax.saxutils.escape(buf)))
    out.write("</data></event>\n")

def print_kv_event(stanza, t, kv, out):
    darray = []
    fm = lambda x: "\"%s\"" if (isinstance(x, str) or isinstance(x, unicode)) and (' ' in x.strip() or '/' in x.strip()) else "%s"
        
    for k, v in kv.items():
        s = [fm(k), fm(v)]
        darray.append("=".join(s) % (k, v))
    
    data = ", ".join(darray)
    send_data(stanza, t, data, out)

