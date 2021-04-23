# Plugin for HAZELCAST Monitoring
This plugin can be used to monitor the Hazelcast application with the use of JMX

#### Prerequisites

* Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin.

* Plugin uses JDK to communicate with JMX MBean to get the metrics for monitoring.

* In the terminal, execute the following command to enable jmx.

	export JAVA_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1099 -Dcom.sun.management.jmxremote.authentication=false -Dcom.sun.management.jmxremote.ssl=false"
	
	Note : Change the port if needed.
	
* To customize the instance name, insert the xml command <instance-name>YOUR_CUSTOM_INSTANCE_NAME</instance-name> in the hazelcast.xml of the $HAZELCAST_HOME/bin folder.

* Download the library Jpype1 module by executing the following command in the terminal.
	pip3 install JPype1

#### Plugin Installation
##### Linux

* Create a directory "hazelcast" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/hazelcast
* Download the files in "hazelcast" folder and place it under the "hazelcast" directory.
* Configure the host, port, username and password in order to monitor.
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

#### Metrics Captured

