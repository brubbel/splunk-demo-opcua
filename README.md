# splunk-demo-opcua

1.0 Feature Overview

OPC UA (OPC Unified Architecture) is a platform-independent industrial standard from opcfoundation.org for communication of industrial automation devices and systems. It is an advanced communication technology for process control, data acquisition and manufacturing automation. This demo-opcua provides users with industrial operations the ability to connect their OPC UA servers with Splunk Enterprise, giving users the advantages of both OPC’s unified architecture and Splunk's analytics capabilities and UI experience. 


1.1 Problem Summary

Splunk does not currently have an add-on (connector) for OPC UA.  This OPC UA connector will give customers a quick method for ingesting their OPC UA data into Splunk. 


1.2 Introduction to Feature

TA_OPCUA provides the following features:

Objects Exploration in UA Server

Data Pulling from Devices managed by UA Server in a scheduled manner

Subscription of events from Devices managed by UA Server

User interface view of connections and configuration management

Alarms notification within UA Server

Optional: UA Server simulator that is intended to be the extension of Data Acquisition and Process Control for custom development


1.3 Capabilities and Assumptions

The implementation of this project follows the specification of the Unified Architecture from opcfoundation.org. The version of the specification is currently 1.03 (2015-10-10). The proposed connector is expected to on the following OPC UA Server products:

https://www.kepware.com/products/kepserverex/suites/opc-connectivity-suite

https://www.unified-automation.com/downloads/opc-ua-servers.

http://www.matrikonopc.com/opc-ua/

https://inductiveautomation.com/products/ignitionopc/overview

https://www.prosysopc.com/products/

1.4 References

[1] http://blogs.splunk.com/2013/10/04/manufacturing-data-acquisition-project-splunk-demo-opcda/

[2] http://blogs.splunk.com/2013/08/29/getting-manufacturing-data-into-splunk/

[3] https://github.com/FreeOpcUa

1.5 Contact

btsay@splunk.com


