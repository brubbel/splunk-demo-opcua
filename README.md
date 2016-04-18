# splunk_demo_opcua

1.0 Feature Overview

OPC UA (OPC Unified Architecture) is a platform-independent industrial standard from opcfoundation.org for communication of industrial automation devices and systems. It is an advanced communication technology for process control, data acquisition and manufacturing automation. This Splunk TA is to provide uers in manufacturing sector to connect their UA servers with Splunk Enterprise while then enabling their systems easy integration with Splunk and are able to leverage its rich analytics and applications.

Although it is not as part of the scopes for now, TA-OPCUA may be a bridge for the users to use Splunk in designing their SCADA dashboard. The purposed features currently include Event Pull and Subscription, Alert Notification and UA Simulation Server (optional).


1.1 Problem Summary

There is no UA connector currently available in the market to support Splunk connectivity with OPC UA. This is the poineering UA connector within Splunk and our commitment of IoT to manufacturing industry that Splunk will keep supporting and developing useful tools for the industry to integrate their systems, devices with Splunk products.


1.2 Introduction to Feature

TA_OPCUA provides features as:

Objects Exploration in UA Server

Data Pulling from Devices managed by UA Server in a scheduled manner.

Subscription of events from Devices managed by UA Server.

User interface view of connections and configuration management.

Alarms notification within UA Server.

UA Server simulator that is optional but intended to be the extension of Data Acquisition and Process Control for customization development. 


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