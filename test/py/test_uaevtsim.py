'''
Created on Apr 16, 2015

@author: btsay
'''
import unittest
import ta_opcua
import splunk_opcua.evtconf as evtconf
#import env

class Test(unittest.TestCase):

    def setUp(self):
        self.fields = evtconf.get_locals().keys()

    def tearDown(self):
        pass

    def testFloatRandomSelect(self):
        evtgen = {}
        for f in self.fields:
            conf = ta_opcua.GET(f, evtconf)
            evtgen[f] = ta_opcua.invoke_object(conf)

        for n, v in evtgen.items():
            print n
            for x in range(10):
                print v.next()
            print "------------------------"

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()