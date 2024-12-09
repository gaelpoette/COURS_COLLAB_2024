set style data linespoints
set grid
set xlabel 'Time'
set ylabel 'Densities of the species'
plot \
'rez_rk4.txt' using 1:2 with linespoints title 'e^-', \
'rez_rk4.txt' using 1:3 with linespoints title 'Ar', \
'rez_rk4.txt' using 1:4 with linespoints title 'B', \
'rez_rk4.txt' using 1:5 with linespoints title 'C', \
'rez_rk4.txt' using 1:6 with linespoints title 'K', \
'rez_rk4.txt' using 1:7 with linespoints title 'L'
pause -1
