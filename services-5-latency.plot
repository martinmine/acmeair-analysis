
set terminal pdf enhanced
set output 'pdf/results-lat5.pdf'
set datafile separator ","


set title "Response time per service (5ms latency)"
set style data histogram
set ylabel 'Response time (ms)'
set xtics rotate by -45
set yrange [0:*]

plot for [COL=4:10:3] resultFile every ::4 using COL:xticlabels(1) title columnheader
