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

hazelcast_metrics={"asyncOperations":"async_operations","completedCount":"completed_count","queueSize":"queue_size","retryCount":"retry_count","runningCount":"running_count","responses.missingCount":"responses_missing_count","responses.normalCount":"responses_normal_count","responses.timeoutCount":"responses_timeout_count","callTimeoutCount":"call_timeout_count","failedBackups":"failed_backups","invocations.pending":"pending_invocations","invocations.usedPercentage":"invocations_used_percentage","operationTimeoutCount":"operation_timeout_count","priorityQueueSize":"priority_queue_size","backupTimeoutMillis":"backup_timeout_millis","backupTimeouts":"backup_timeouts","delayedExecutionCount":"delayed_execution_count","heartbeatBroadcastPeriodMillis":"hearbeat_broadcast_period_millis","heartbeatPacketsSent":"heartbeat_packets_sent","heartbeatPacketsReceived":"heartbeat_packets_received","normalTimeouts":"normal_timeouts","invocationScanPeriodMillis":"invocation_scan_period_millis","invocationTimeoutMillis":"invocation_timeout_millis","parkQueueCount":"park_queue_count","totalParkedOperationCount":"total_parked_operation_count"}

metric_units={"invocations_used_percentage":"%","backup_timeout_millis":"ms","heartbeat_broadcast_period_millis":"ms","invocation_timeout_millis":"ms","invocation_scan_period_millis":"ms"}

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
		metrics={"com.hazelcast:type=Metrics,instance="+instance+",prefix=operation":["asyncOperations","completedCount","queueSize","retryCount","runningCount","responses.missingCount","responses.normalCount","responses.timeoutCount","callTimeoutCount","failedBackups","invocations.pending","invocations.usedPercentage","operationTimeoutCount","priorityQueueSize"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=operation.invocations":["backupTimeoutMillis","backupTimeouts","delayedExecutionCount","heartbeatBroadcastPeriodMillis","heartbeatPacketsSent","heartbeatPacketsReceived","normalTimeouts","invocationScanPeriodMillis","invocationTimeoutMillis"],"com.hazelcast:type=Metrics,instance="+instance+",prefix=operation.parker":["parkQueueCount","totalParkedOperationCount"]}
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
