#!/usr/bin/python3

import os
import datetime

# This script filters CoAP requests with response times <80, 200> with latency 0

now = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
resultFile = "filtered-requests.csv"
with open(resultFile, "w+") as summaryFile:
    for directory in sorted(os.listdir('.')):
        serviceInfo = directory.split('-')
        
        if (os.path.isdir("./" + directory)):
            for serviceName in os.listdir("./" + directory):
                if (serviceName.endswith(".jtl")):
                    requestMap = {}

                    with open("./" + directory + "/" + serviceName) as logFile: 
                        print("> " + directory)
                        if (serviceInfo[0] == 'coap' and serviceInfo[1] == '0'):
                            for logLine in logFile:
                                logAttributes = logLine.split(',')

                                if (int(logAttributes[1]) > 80 and int(logAttributes[1]) < 200):
                                    summaryFile.write(logAttributes[0] + ' ') # Time
                                    summaryFile.write(logAttributes[1]) # Response time
                                    summaryFile.write('\n')

print("=> " + resultFile)