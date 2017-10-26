set terminal pdf enhanced
set output 'pdf/coap-frequency.pdf'


set title "Request frequency "
set ylabel 'Response time (ms)'
set xlabel 'Time'
set format x ""
#set yrange [120:165]

plot 'filtered-requests.csv' w p ls 1 notitle
