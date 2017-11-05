#!/usr/bin/python3

import json
import os
import sys
import datetime
import statistics
import subprocess

import mysql.connector

cnx = mysql.connector.connect(user='root', password='123',
                              host='127.0.0.1',
                              database='acmeair')

createImportRecord = ("INSERT INTO import (date) VALUES (%s)")
createNetworkRecord = ("INSERT INTO network "
                "(importId, protocol, latency, serviceName, interface, txBytes, txPackets, rxBytes, rxPackets) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
createRequestRecord = ("INSERT INTO request "
                "(importId, protocol, latency, timestamp, responseTime, testName, responseCode, responseLength) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
createCpuUsageRecord = ("INSERT INTO cpuUsage (importId, time, service, latency, protocol, cpuUsage) "
                "VALUES (%s, %s, %s, %s, %s, %s)")

now = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")

cursor = cnx.cursor()

#cursor.execute(createImportRecord, [now])
#cnx.commit()
importId = '1' #cursor.lastrowid

for directory in sorted(os.listdir('.')):
    serviceInfo = directory.split('-')
    
    if (os.path.isdir("./" + directory) and directory != ".git"):
        print("==== " + directory + " ====")
        for serviceName in os.listdir("./" + directory):
            if (os.path.isdir("./" + directory + "/" + serviceName)):
                print("Found logs for service " + serviceName)
                logEntries = sorted(os.listdir("./" + directory + "/" + serviceName))

                networkLogs = [a for a in logEntries if a.startswith("network")]
                systemLogs = [a for a in logEntries if a.startswith("system")]

                firstNetworkLog = networkLogs[0]
                lastNetworkLog = networkLogs[-1]

                for systemLog in systemLogs:
                    logInfo = systemLog.split('-')
                    with open("./" + directory + "/" + serviceName  + "/" + systemLog) as systemLogFile:
                        logContents = json.load(systemLogFile)
                        logTime = logInfo[1][:4] + '-' + logInfo[1][4:6] + '-' + logInfo[1][6:8] + ' ' + logInfo[2][:2] + ':' + logInfo[2][2:4] + ':' + logInfo[2][4:6]
                        cursor.execute(createCpuUsageRecord, (importId, logTime, serviceName, serviceInfo[1], serviceInfo[0], str(logContents['systemCpuLoad'])))

                cnx.commit()

                with open("./" + directory + "/" + serviceName  + "/" + networkLogs[0]) as firstNetworkLogF, open("./" + directory + "/" + serviceName  + "/" + networkLogs[-1]) as lastNetworkLogF:
                    firstNetworkLog = [a for a in json.load(firstNetworkLogF) if a['name'] == "eth0"][0]
                    lastNetworkLog = [a for a in json.load(lastNetworkLogF) if a['name'] == "eth0"][0]

                    # (importId, protocol, latency, serviceName, interface, txBytes, txPackets, rxBytes, rxPackets)
                    #           Protocol,Latency,Service,Tx bytes,Tx packets,Rx bytes,Rx Packets

                    txBytes = int(lastNetworkLog['transmit']['bytes']) - int(firstNetworkLog['transmit']['bytes'])
                    txPackets = int(lastNetworkLog['transmit']['packets']) - int(firstNetworkLog['transmit']['packets'])
                    rxBytes = int(lastNetworkLog['receive']['bytes']) - int(firstNetworkLog['receive']['bytes'])
                    rxPackets = int(lastNetworkLog['receive']['packets']) - int(firstNetworkLog['receive']['packets'])

                    cursor.execute(createNetworkRecord, (importId, serviceInfo[0], serviceInfo[1], serviceName, "eth0", str(txBytes), str(txPackets), str(rxBytes), str(rxPackets)))
                    cnx.commit()

            if (serviceName.endswith(".jtl")):
                print("Inserting requests for service " + serviceName)
                with open("./" + directory + "/" + serviceName) as logFile: 
                    for logLine in logFile:
                        logAttr = logLine.split(',')
                        # 1507809917393,68,Login,200,OK,Thread Group 1-1,text,true,371,1,1,68

                        # (importId, protocol, latency, timestamp, responseTime, testName, responseCode, responseLength)
                        cursor.execute(createRequestRecord, (importId, serviceInfo[0], serviceInfo[1], logAttr[0], logAttr[1], logAttr[2], logAttr[3], logAttr[8]))
                        cnx.commit()
        
cursor.close()
cnx.close()

