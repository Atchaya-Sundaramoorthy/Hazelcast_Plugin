#!/usr/bin/python3

import json

PLUGIN_VERSION=1
HEARTBEAT="true"

HOST="localhost"
PORT="1099"
user=""
passw=""
instance=""
jvmpath="/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so"

hazelcast_metrics={"totalRegistrations":"total_client_registrations","size":"cluster_size","eventQueueSize":"event_queue_size","eventsProcessed":"events_processed","queueCapacity":"queue_capacity","rejectedCount":"rejected_count","syncDeliveryFailureCount":"sync_delivery_failure_count","totalFailureCount":"total_failure_count","availableProcessors":"available_processors","uptime":"uptime","bytesReceived":"bytes_received","bytesSend":"bytes_send","packetsReceived":"packets_received","packetsSend":"packets_send","acceptedSocketCount":"accepted_socket_count","activeCount":"active_count","closedCount":"closed_count","clientCount":"client_count","connectionListenerCount":"connection_listener_count","count":"count","inProgressCount":"in_progress_count","openedCount":"opened_count","textCount":"text_count","clusterTimeDiff":"cluster_time_diff","clusterUpTime":"cluster_up_time"}

metric_units={"bytes_send":"byte","bytes_received":"byte","cluster_up_time":"ms"}

def get_data():
	result={}
	result['plugin_version']=PLUGIN_VERSION
	result['heartbeat_required']=HEARTBEAT
	result['units']=metric_units
	
	try:
		import jpype
		from jpype import java
		from jpype import javax
		url="service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi" %(HOST,PORT)
		jpype.startJVM(jvmpath)
		jhash=java.util.HashMap()
		jarray=jpype.JArray(java.lang.String)([user,passw])
		jhash.put(javax.management.remote.JMXConnector.CREDENTIALS,jarray);
		jmxurl=javax.management.remote.JMXServiceURL(url)
		jmxsoc=javax.management.remote.JMXConnectorFactory.connect(jmxurl,jhash)
		connection=jmxsoc.getMBeanServerConnection();
		metrics={"com.hazelcast:type=Metrics,instance="+instance+",prefix=client.endpoint":["totalRegistrations"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=cluster":["size"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=event":["eventQueueSize","eventsProcessed","queueCapacity","rejectedCount","syncDeliveryFailureCount","totalFailureCount"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=runtime":["availableProcessors","uptime"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=tcp":["bytesReceived","bytesSend","packetsReceived","packetsSend"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=tcp.connection":["acceptedSocketCount","activeCount","closedCount","clientCount","connectionListenerCount","count","inProgressCount","openedCount","textCount"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=cluster.clock":["clusterTimeDiff","clusterUpTime"]}
		for metric in metrics:
			for i in metrics[metric]:
				metric_value=connection.getAttribute(javax.management.ObjectName(metric),i)
				result[hazelcast_metrics[i]]=metric_value
		
	except Exception as e:
		result["status"]=0
		result["msg"]=str(e)
		
	return result
	
if __name__=="__main__":
	import argparse
	
	parser=argparse.ArgumentParser()
	parser.add_argument('--host',help="Host Name to connect",type=str)
	parser.add_argument('--port',help="Port to connect",type=int)
	parser.add_argument('--user_name',help="UserName for Authentication",type=str)
	parser.add_argument('--passw',help="Password for authentication",type=str)
	parser.add_argument('--instance',help="Instance for Objects",type=str)
	parser.add_argument('--jvmpath',help="JVM Path for Starting JVM",type=str)
	
	args=parser.parse_args()
	
	if args.host:
		HOST=args.host
	if args.port:
		PORT=args.port
	if args.user_name:
		user=args.user_name
	if args.passw:
		passw=args.passw
	if args.instance:
		instance=args.instance
	if args.jvmpath:
		jvmpath=args.jvmpath
		
	data=get_data()
	print(json.dumps(data,indent=4))
