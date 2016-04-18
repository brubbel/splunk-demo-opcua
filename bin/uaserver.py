
import csv
import os
from collections import OrderedDict

def data_dir():
    p = os.path.realpath(__file__)
    return os.path.abspath(os.path.join(p, os.pardir, os.pardir, "data"))
    
class OrderedDictReader:
    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect="excel", *args, **kwds):
        self._fieldnames = fieldnames   # list of keys for the dict
        self.restkey = restkey          # key to catch long rows
        self.restval = restval          # default value for short rows
        self.reader = csv.reader(f, dialect, *args, **kwds)
        self.dialect = dialect
        self.line_num = 0

    def __iter__(self):
        return self

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            try:
                self._fieldnames = self.reader.next()
            except StopIteration:
                pass
        self.line_num = self.reader.line_num
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value):
        self._fieldnames = value

    def next(self):
        if self.line_num == 0:
            # Used only for its side effect.
            self.fieldnames
        row = self.reader.next()
        self.line_num = self.reader.line_num

        # unlike the basic reader, we prefer not to return blanks,
        # because we will typically wind up with a dict full of None
        # values
        while row == []:
            row = self.reader.next()
        d = OrderedDict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval
        return d


class DataChannel(object):

    def __init__(self, data, count=10, interval=1, line_num=0):
        self.data = data
        self.line_num = line_num
        self.count = count
        self.interval = interval
        
    def __iter__(self):
        return self
    
    def get_current_line_num(self):
        return self.line_num
    
    def next(self):
        d = []
        
        for n in range(self.count):
            dd = self.data[self.line_num]
            self.line_num = self.line_num + 1
            if self.line_num >= len (self.data):
                self.line_num = 0
                
            d.append(dd)
            
        return d
        
import json
        
def get_metadata(sep='.'):
    meta = os.path.join(data_dir(), "meta.json")
    d = {}
    with open(meta, 'rU') as data_file:    
        data = json.load(data_file)
        for n,v in data.items():
            for nn, vv in v.items():
                for vvv in vv:
                    d[vvv] = "%s%s%s%s%s" % (n, sep, nn, sep, vvv)
        data_file.close()
                    
    return d
 

class AlertEventChannel(object):

    def __init__(self, data, count=10, interval=1, line_num=0):
        self.data = data
        self.line_num = line_num
        self.count = count
        self.interval = interval
        
    def get_current_line_num(self):
        return self.line_num
    
    def __iter__(self):
        return self
    
    def next(self):
        d = []
        
        for n in range(self.count):
            dd = self.data[self.line_num]
            self.line_num = self.line_num + 1
            if self.line_num >= len (self.data):
                self.line_num = 0
                
            d.append(dd)
            
        return d
    

