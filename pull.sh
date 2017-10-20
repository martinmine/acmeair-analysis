#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Missing argument [filename]"
    exit 1
fi

ssh acmeair-jmeter1 zip -r $1.zip monitor-data
scp acmeair-jmeter1:$1.zip .
unzip $1.zip
mv monitor-data $1
cd $1
../log-pull.sh

echo "Logs extracted in $1"
