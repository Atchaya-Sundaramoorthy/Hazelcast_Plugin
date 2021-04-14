# Hazelcast_Plugin
Plugin to monitor Hazelcast

# Prerequesites:
1. Install the Hazelcast Application properly.
	
2. To enable jmx, 
	1. In the terminal, execute the following command.
		
		export JAVA_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1099 -Dcom.sun.management.jmxremote.authentication=false -Dcom.sun.management.jmxremote.ssl=false"
			
		Note: Change the host name and port number if needed.
	
3. Since hazelcast uses different instance names everytime it gets started, we need to provide a custom instance name.  For that, 
	
	Insert the lines <instance-name>YOUR_CUSTOM_INSTANCE_NAME</instance-name> in the hazelcast.xml file of $HAZELCAST_HOME/bin folder.
			
4. Now, you can run the hazelcast start script inside the $HAZELCAST_HOME/bin folder by executing ./start.sh command.
	
5. Now jmx is enabled for hazelcast.
	
6. Download the hazelcast plugin programs "hazelcast.py" and "hazelcast_operation.py".
	
7. For multiple configurations, download the "hazelcast.cfg" and "hazelcast_operation.cfg" documents and change the hostname, port number, user name and password accordingly.
