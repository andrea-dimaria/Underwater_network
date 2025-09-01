for i in {0..14}
    do
	    sleep 2
	    echo 1, 0, 0 > ~/AMUSE/synchronization.csv
	    ns AMUSE_Des3.tcl
    done
