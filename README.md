Network evolve

The code files udpopnet_random.py and udpopnet_evovle_stable.py were written in Python 2.7.10.

udpopnet_random.py generates networks (number of replicates defaults to 100) with random topologies and nodes between 2 and 20. Various summary parameters, including the critical migration rate, for each of the randomly genereated networks are output as "randomnetoutput.txt".
udpopnet_evolve_stable.py generates network with a specified number of nodes and evolves the topology towards one with a greater critical migration rate, i.e. greater stability. The output is given in file "bestnetoutput.txt".
