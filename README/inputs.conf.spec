# Copyright (C) 2005-2015 Splunk Inc. All Rights Reserved.
# The file contains the specification for all db connect modular inputs
# * mi_opcua - the moudular input that facilitates OPC UA Client against Kepware OPC Server.

[mi_opcua://default]

description = <value>
* Description for this opc client

connection = <value>
* Indicates the connection parameter to the opc server.

username = <value>
* Optional user name to login the opc server.
* Leave it empty when OPC server does not set up user authentication.

password = <value>
* Password while username is set.
* Leave it empty when OPC server does not set up user authentication.

connection_timeout = <value>
* Indicates the connection timeout.
* Examples: 30

measures = <value>
* Indicates the wildcards of selected resources to collect.
* Examples: Objects:S*:~A*

metrics_spec = <value>
* Indicates the specification of metrics for displaying additional fields.
* Leave it empty when no specification is defined.

[mi_opcua_subscription://default]

description = <value>
* Description for this opc client

connection = <value>
* Indicates the connection parameter to the opc server.

username = <value>
* Optional user name to login the opc server.
* Leave it empty when OPC server does not set up user authentication.

password = <value>
* Password while username is set.
* Leave it empty when OPC server does not set up user authentication.

connection_timeout = <value>
* Indicates the connection timeout.

collect_duration = <value>
* Indicates the collection duration in milliseconds.
* Example: 30

measures = <value>
* Indicates the wildcards of selected resources to collect.
* Examples: Objects:S*:~A*


[mi_opcua_event://default]

description = <value>
* Description for this opc client

connection = <value>
* Indicates the connection parameter to the opc server.

username = <value>
* Optional user name to login the opc server.
* Leave it empty when OPC server does not set up user authentication.

password = <value>
* Password while username is set.
* Leave it empty when OPC server does not set up user authentication.

connection_timeout = <value>
* Indicates the connection timeout.

collect_duration = <value>
* Indicates the collection duration in milliseconds.

[mi_uaserver://default]

description = <value>
* Description for this ua server

count = <value>
* Indicates the event count within one period.

serverpath = <value>
* The server path for this server.

namespace = <value>
* The namespace of the services.

serverport = <value>
* The port of the service server.

nodefile = <value>
* Json node structure file.

datafile = <value>
* The data to playback.

username = <value>
* User account for this server.
* Leave it empty when OPC server does not set up user authentication.

password = <value>
* User password for this account.

connection_timeout = <value>
* Connection timeout.

[mi_uaserver2://default]

description = <value>
* Description for this ua server

serverpath = <value>
* The server path for this server.

namespace = <value>
* The namespace of the services.

serverport = <value>
* The port of the service server.

nodefile = <value>
* Json node structure file.

username = <value>
* User account for this server.
* Leave it empty when OPC server does not set up user authentication.

password = <value>
* User password for this account.
* Leave it empty when OPC server does not set up user authentication.

connection_timeout = <value>
* Connection timeout.

[mi_iot_event_gen://default]

description = <value>
* Description for this ua server

assets = <value>
* The configuration of assets.

metrics = <value>
* The configuration of metrics.

conditions = <value>
* The configuration of conditions.
