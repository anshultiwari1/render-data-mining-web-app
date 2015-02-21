tq_bin='/home/anshul/dev/python/Tractor-2.0/bin/tq'

export TRACTOR_ENGINE=fox:1503

$tq_bin tasks "jid=877" -c wtime --nh | tail -n+2 | awk '{print $1}'