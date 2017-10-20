
set terminal pdf enhanced
set output 'pdf/network.pdf'
set datafile separator ";"


set title "Sent/received bytes"
set style data histogram
set ylabel 'bytes'

plot for [COL=2:64:22] 'networkdata-2017-10-09-17.16.22-transformed.csv' every 2::2 using COL:xticlabels(1) title columnheader
