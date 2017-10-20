set terminal pdf enhanced
set output 'pdf/network-packets-auth-service-liberty1.pdf'

#set terminal epslatex color
#set out 'tex/packets-nginx1.tex'

set datafile separator ","


set title "Transmitted packets (auth-service-liberty1)"
set style data histogram
set ylabel 'packets'
set format y '%.0s%c'
set yrange [0:*]

plot for [COL=2:64:21] networkData every 2::3 using COL:xticlabels(1) title columnheader
