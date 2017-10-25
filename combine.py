#!/usr/bin/python3

import os
import datetime

# This script is used to combine all request logs to one file for analysis in SPSS

now = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
resultFile = "agregated-requests.csv"
with open(resultFile, "a") as summaryFile:
    # Header:
    summaryFile.write("Protocol,Latency,Case,Response time,Response code\n")
    for directory in sorted(os.listdir('.')):
        serviceInfo = directory.split('-')
        
        if (os.path.isdir("./" + directory)):
            for serviceName in os.listdir("./" + directory):
                if (serviceName.endswith(".jtl")):
                    requestMap = {}

                    with open("./" + directory + "/" + serviceName) as logFile: 
                        print("> " + directory)
                        for logLine in logFile:
                            logAttributes = logLine.split(',')

                            summaryFile.write(serviceInfo[0] + ',') # Protocol
                            summaryFile.write(serviceInfo[1] + ',') # Latency

                            summaryFile.write(logAttributes[2] + ',') # Test case
                            summaryFile.write(logAttributes[1] + ',') # Response time
                            summaryFile.write(logAttributes[3]) # HTTP response code

                            summaryFile.write('\n')

print("=> " + resultFile)