set sty da l;set grid; set xl 'time'; set yl 'densities of the species'; 

plot 'euler.txt' t 'e^- ref', '' u 1:3 t 'Ar ref', '' u 1:4 t 'B ref', 'rez.txt' lt 1 w lp  t 'e^-','' u 1:3 lt 3 w lp t 'Ar','' u 1:4 lt 4 w lp t 'B';


pause -1