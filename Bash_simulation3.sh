#change according to the number of episodes in AMUSE3 script
for i in {0..1}
    do
	    sleep 2
	    echo 1, 0 > ~/AMUSE/synchronization.csv
	    ns AMUSE_Des3.tcl
    done
