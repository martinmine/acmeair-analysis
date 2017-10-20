set terminal pdf enhanced
set output 'pdf/network-bytes-auth-service-liberty1.pdf'
set datafile separator ","


set title "Transmitted bytes (auth-service-liberty1)"
set style data histogram
set format y '%.0s%cB'
set yrange [0:*]

plot for [COL=2:64:21] networkData every 2::2 using COL:xticlabels(1) title columnheader
