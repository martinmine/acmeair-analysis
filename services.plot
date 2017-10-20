
set terminal pdf enhanced
set output 'results.pdf'
set datafile separator ";"


set title "Response time per service"
set style data histogram
set ylabel 'Response time (ms)'

plot for [COL=2:10:3] 'results-2017-10-09-11.22.38-transformed.csv' every ::4 using COL:xticlabels(1) title columnheader
