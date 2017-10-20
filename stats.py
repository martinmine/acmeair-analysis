#!/usr/bin/python3

import json
import os
import sys
import datetime
import statistics
import subprocess


now = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
with open("results-" + now + ".csv", "a") as summaryFile, open("results-" + now + "-err.csv", "a") as errorFile, open("networkdata-" + now + ".csv", "a") as networkFile:
    summaryFile.write("Protocol,Latency,Requests,Average,Book Flight,Cancel Booking,List Bookings,Login,Query Flight,Update Customer,View Profile Information,logout\n")
    errorFile.write("Protocol,Latency,Requests,Average,Book Flight,Cancel Booking,List Bookings,Login,Query Flight,Update Customer,View Profile Information,logout\n")
    networkFile.write("Protocol,Latency,Service,Tx bytes,Tx packets,Rx bytes,Rx Packets\n")
    for directory in sorted(os.listdir('.')):
        serviceInfo = directory.split('-')
        
        if (os.path.isdir("./" + directory)):
            #print("==== " + directory + " ====")
            for serviceName in os.listdir("./" + directory):
                if (os.path.isdir("./" + directory + "/" + serviceName)):
                    print("Found logs for service " + serviceName)
                    logEntries = sorted(os.listdir("./" + directory + "/" + serviceName))

                    networkLogs = [a for a in logEntries if a.startswith("network")]
                    systemLogs = [a for a in logEntries if a.startswith("system")]

                    firstNetworkLog = networkLogs[0]
                    lastNetworkLog = networkLogs[-1]

                    with open("./" + directory + "/" + serviceName  + "/" + networkLogs[0]) as firstNetworkLogF, open("./" + directory + "/" + serviceName  + "/" + networkLogs[-1]) as lastNetworkLogF:
                        firstNetworkLog = [a for a in json.load(firstNetworkLogF) if a['name'] == "eth0"][0]
                        lastNetworkLog = [a for a in json.load(lastNetworkLogF) if a['name'] == "eth0"][0]

                        networkFile.write(serviceInfo[0] + ',' + serviceInfo[1] +  ',')
                        networkFile.write(serviceName + ',')
                        networkFile.write(str(int(lastNetworkLog['transmit']['bytes']) - int(firstNetworkLog['transmit']['bytes'])) + ",")
                        networkFile.write(str(int(lastNetworkLog['transmit']['packets']) - int(firstNetworkLog['transmit']['packets'])) + ",")

                        networkFile.write(str(int(lastNetworkLog['receive']['bytes']) - int(firstNetworkLog['receive']['bytes'])) + ",")
                        networkFile.write(str(int(lastNetworkLog['receive']['packets']) - int(firstNetworkLog['receive']['packets'])) + ",\n")

                        #print("Total trasnmit bytes: " + str(int(lastNetworkLog['transmit']['bytes']) - int(firstNetworkLog['transmit']['bytes'])))
                        #print("Total trasnmit packets: " + str(int(lastNetworkLog['transmit']['packets']) - int(firstNetworkLog['transmit']['packets'])))
                        ###print("Total errs: " + str(int(lastNetworkLog['transmit']['errs']) - int(firstNetworkLog['transmit']['errs'])))
                        ###print("Total drop: " + str(int(lastNetworkLog['transmit']['drop']) - int(firstNetworkLog['transmit']['drop'])))
                        ###print("Total fifo: " + str(int(lastNetworkLog['transmit']['fifo']) - int(firstNetworkLog['transmit']['fifo'])))
                        ###print("Total frame: " + str(int(lastNetworkLog['transmit']['frame']) - int(firstNetworkLog['transmit']['frame'])))
                        ###print("Total compressed: " + str(int(lastNetworkLog['transmit']['compressed']) - int(firstNetworkLog['transmit']['compressed'])))
                        ###print("Total multicast: " + str(int(lastNetworkLog['transmit']['multicast']) - int(firstNetworkLog['transmit']['multicast'])))
                        ###print("Total carrier: " + str(int(lastNetworkLog['transmit']['carrier']) - int(firstNetworkLog['transmit']['carrier'])))
    ##
                        #print("Total receive bytes: " + str(int(lastNetworkLog['receive']['bytes']) - int(firstNetworkLog['receive']['bytes'])))
                        #print("Total receive packets: " + str(int(lastNetworkLog['receive']['packets']) - int(firstNetworkLog['receive']['packets'])))
                        #print("Total errs: " + str(int(lastNetworkLog['receive']['errs']) - int(firstNetworkLog['receive']['errs'])))
                        #print("Total drop: " + str(int(lastNetworkLog['receive']['drop']) - int(firstNetworkLog['receive']['drop'])))
                        #print("Total fifo: " + str(int(lastNetworkLog['receive']['fifo']) - int(firstNetworkLog['receive']['fifo'])))
                        #print("Total frame: " + str(int(lastNetworkLog['receive']['frame']) - int(firstNetworkLog['receive']['frame'])))
                        #print("Total compressed: " + str(int(lastNetworkLog['receive']['compressed']) - int(firstNetworkLog['receive']['compressed'])))
                        #print("Total multicast: " + str(int(lastNetworkLog['receive']['multicast']) - int(firstNetworkLog['receive']['multicast'])))
                        #print("Total carrier: " + str(int(lastNetworkLog['receive']['carrier']) - int(firstNetworkLog['receive']['carrier'])))
                    #print("First network log was " + firstNetworkLog)
                    #print("Last network log was " + lastNetworkLog)



                    #for logEntry in networkLogs:
                    #    print(logEntry)
                    #    with open("./" + directory + serviceName  + "/" + logEntry) as logEntryFile:
                    #        log = json.load(logEntryFile)
                    #        print("Loaded " + logEntry)
                if (serviceName.endswith(".jtl")):
                    requestMap = {}
                    

                    totalRequests = 0
                    totalRequestTime = 0
                    with open("./" + directory + "/" + serviceName) as logFile: 
                        
                        for logLine in logFile:
                            totalRequests = totalRequests + 1
                            logAttributes = logLine.split(',')

                            try:

                                if logAttributes[2] in requestMap:
                                    requestMap[logAttributes[2]].append(int(logAttributes[1]))
                                else:
                                    requestMap[logAttributes[2]] = [int(logAttributes[1])]

                                totalRequestTime = totalRequestTime + int(logAttributes[1])
                            except ValueError:
                                print ("Error reading line " + str(totalRequests))
                                print (logLine)

                    avgs = []
                    stddevs = []
                    for groupName in sorted(requestMap.keys()):
                        avg = sum(requestMap[groupName]) / len(requestMap[groupName])
                        stdDev = statistics.stdev(requestMap[groupName])
                        #print("Average response time for " + groupName + ": " + str(avg) + " (std.dev: " + str(stdDev) + ")")
                        avgs.append(avg)
                        stddevs.append(stdDev)

                    totalAvg = totalRequestTime / totalRequests
                    summaryFile.write(serviceInfo[0] + ',' + serviceInfo[1] +  ',' + str(totalRequests) + "," + str(totalAvg) + ','.join(map(str, avgs)) + "\n")
                    errorFile.write(serviceInfo[0] + ',' + serviceInfo[1] +  ',' + str(totalRequests) + "," + str(totalAvg) + ','.join(map(str, stddevs)) + "\n")
                
                    

print("wrote to results-" + now + ".csv")
subprocess.call(["/usr/bin/python", "./transform.py", "results-" + now + ".csv", "results-" + now + "-transformed.csv"])
subprocess.call(["/usr/bin/python", "./transform.py", "networkdata-" + now + ".csv", "networkdata-" + now + "-transformed.csv"])
print("transformed> results-" + now + "-transformed.csv")

subprocess.call(["./plotall.sh", now])

