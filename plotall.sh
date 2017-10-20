#!/bin/bash

set -e

overview="results-$1-transformed.csv"
network="networkdata-$1-transformed.csv"

gnuplot -e "resultFile='$overview'" services-0-latency.plot
gnuplot -e "resultFile='$overview'" services-2-latency.plot
gnuplot -e "resultFile='$overview'" services-5-latency.plot
gnuplot -e "networkData='$network'" network-bytes.plot
gnuplot -e "networkData='$network'" network-packets.plot
echo "done"
