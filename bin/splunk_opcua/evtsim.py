
"""
class yrange:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()
"""

import random
import re
import ta_opcua

class Field(object):
    
    def __iter__(self):
        return self
        
    def next(self):
        pass
    
    
class RandomSelect(Field):
    
    def __init__(self, values, seed=123, freq_sep=":", val_sep=","):
        super(Field, self).__init__()
        self.seed = seed
        self.freq_sep = freq_sep
        self.val_sep = val_sep
        
        vals = values if isinstance(values, list) else values.split(self.val_sep)
        
        self.values = []
        self.ratio = []
        for val in vals:
            vr = str(val).split(self.freq_sep)
            if len(vr)==2:
                self.ratio.append(int(vr[1]))
            else:
                self.ratio.append(1)
                
            self.values.append(vr[0])
            
    def get_random(self):
        c = 0
        m = []
        s = 0
        
        for r in self.ratio:
            c = c + r
            for n in range(0, r):
                m.append(s)
            
            s = s + 1
        
        x = random.randint(0, c-1)
        
        return m[x]
        
    def next(self):
        r = self.get_random()
        return self.values[r]
    
    
class SequenceRotate(Field):
    
    def __init__(self, values, freq_sep=":", val_sep=","):
        super(Field, self).__init__()
        self.freq_sep = freq_sep
        self.val_sep = val_sep
        
        vals = values if isinstance(values, list) else values.split(self.val_sep)
        
        self.values = []
        self.ratio = []
        
        for n in range(0, len(vals)):
            vr = vals[n].split(self.freq_sep)
            c = int(vr[1]) if len(vr)==2 else 1
            for m in range(0, c):
                self.ratio.append(n)
                
            self.values.append(vr[0])
        
        self.current = 0
        
    def get(self):
        x = self.ratio[self.current]
        self.current = (self.current+1) % len(self.ratio)
        return x
        
    def next(self):
        return self.values[self.get()]


class RangeSelect(Field):
    
    def __init__(self, range, duration=1, val_sep=":"):
        self.val_sep = val_sep
        self.duration = duration
        values = range.split(self.val_sep)
        self.start = int(values[0].strip())
        self.current = self.start
        
        if len(values) == 2:
            if values[1].strip() == "-":
                self.end = "-"   # endless
            else:
                self.end = int(values[1].strip())
                if self.end < self.start:
                    raise ValueError("Invalid Range starts from %s end %s." % (self.start, self.end))
    
    def next(self):
        v = self.current
        self.current = v + self.duration
        if self.end == "-" or v <= self.end:
            return v
        else:
            self.current = self.start
            return self.next()

class RangeRotate(RangeSelect):
    def next(self):
        v = self.current
        self.current = v + self.duration
        if self.end == "-" or v < self.end:
            return v
        else:
            self.current = self.start
            return self.next()


class CompositeField(Field):

    def __init__(self, value):
        super(Field, self).__init__()
        self.value = value
        self.vars = {}        
        for f in self.parse_tokens(value):
            self.vars[f] = ta_opcua.invoke_object(ta_opcua.GET(f, ta_opcua))

        
    def parse_tokens(self, val):
        return [v.lstrip("<").rstrip(">") for v in re.findall("\<\w+\>", val)]

    
    def next(self):
        val = self.value
        for v in self.vars:
            x = next(self.vars[v])
            val = val.replace("<%s>" % v, str(x))
            
        return val


def random_select(conf):
    return RandomSelect(conf.get("values"), int(conf.get("seed", "123")), conf.get("freq_sep", ":"), conf.get("val_sep", ","))

def number_range_select(conf):
    duration = int(conf.get("duration", "1"))
    return RangeSelect(conf.get("range"), duration, conf.get("val_sep", ":"))

def random_number_range_select(conf):
    duration = int(conf.get("duration", "1"))
    val_sep = conf.get("val_sep", ":")
    r = conf.get("range").split(val_sep)
    vals = range(int(r[0]), int(r[1])+duration, duration)
        
    return RandomSelect(vals)

def random_float_range_select(conf):
    duration = int(conf.get("duration", "1"))
    factor = int(conf.get("factor", "10"))
    val_sep = conf.get("val_sep", ":")
    r = conf.get("range").split(val_sep)
    
    a = int(float(r[0])*factor)
    b = int(float(r[1])*factor)
    
    vals = [float(x)/factor for x in range(a, b, duration)]
    
    return RandomSelect(vals)

def number_range_rotate(conf):
    duration = int(conf.get("duration", "1"))
    val_sep = conf.get("val_sep", ":")
    r = conf.get("range").split(val_sep)
    vals = range(int(r[0]), int(r[1]), duration)
        
    return SequenceRotate(vals)

def float_range_rotate(conf):
    duration = int(conf.get("duration", "1"))
    factor = int(conf.get("factor", "10"))
    val_sep = conf.get("val_sep", ":")
    r = conf.get("range").split(val_sep)

    a = int(float(r[0])*factor)
    b = int(float(r[1])*factor)
    
    vals = [float(x)/factor for x in range(a, b, duration)]
        
    return SequenceRotate(vals)

def range_rotate(conf):
    duration = int(conf.get("duration", "1"))
    return RangeRotate(conf.get("values"), duration, conf.get("val_sep", ":"))

def sequence_rotate(conf):
    return SequenceRotate(conf.get("values"), conf.get("freq_sep", ":"), conf.get("val_sep", ","))

def random_select_from_file(conf):
    fname = conf.get("file")
    with open(fname) as f:
        values = f.readlines()
    
    return RandomSelect(values, conf.get("seed"), conf.get("freq_sep", ":"), conf.get("val_sep", ","))

def sequence_rotate_from_file(conf):
    fname = conf.get("file")
    with open(fname) as f:
        values = f.readlines()
    f.close()
    
    return SequenceRotate(values, conf.get("freq_sep", ":"), conf.get("val_sep", ","))

def composite_field(conf):
    return CompositeField(conf.get("value"))

