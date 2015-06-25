# Evolve a fully connected network to have a minimum number of edges
import copy
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

# number of nodes in the network
nodes = 10 

# initial fully connected network represented as a matrix
net = [[1 for x in range(nodes)] for x in range(nodes)] 
for i in range(0, nodes): 
	net[i][i]=0

# count the number of edges
def countedge(net):
	edges=0
	for i in range(0, nodes):
		for j in range(0, nodes):
			edges += net[i][j]
	return edges/2

# check if the network is fully interconnected
def fullconnectcheck(net):
	connected = [0 for x in range(nodes)]
	connected[0]=1
	current=0

	for k in range(0, nodes): 
		for j in range(0, nodes):
			current = j
			if(connected[j] == 1):
				for i in range(0, nodes): # walks through and finds connections to first node
					if(i != current):
						if(net[current][i]==1):
							connected[i]=1
	connectcount=0
	for j in range(0, nodes):
		if(connected[j]==1):
			connectcount=connectcount+1
	if(connectcount == nodes):
		# fully connected
		return 1
	else: 
		# not connected
		return 0

# make random change to network connections
def netevolve(modifynet):
	# add or remove
	choice = random.randrange(0, 2)	
	# pick a random position
	pick = random.randrange(0, nodes)
	if(choice==0):
		# add a connection to that node
		reconnect=0
		howmany=0
		for j in range(0, nodes):
			howmany=howmany+modifynet[pick][j]

		while(reconnect==0):
			if(howmany == nodes-1):
				reconnect=1
			connectpick = pick
			while(connectpick == pick):
				connectpick = random.randrange(0, nodes)
			if(modifynet[pick][connectpick]==0):
				modifynet[pick][connectpick]=1
				modifynet[connectpick][pick]=1
				# check if fully connected
				if(fullconnectcheck(modifynet)):
					reconnect=1 # done and can exit
				else: # reset and try again
					modifynet[pick][connectpick]=0
					modifynet[connectpick][pick]=0
	else:
		# break a connection from that node
		broken=0
		while(broken==0):
			breakpick = random.randrange(0, nodes)
			if(modifynet[pick][breakpick]==1):
				modifynet[pick][breakpick]=0
				modifynet[breakpick][pick]=0
				# check if fully connected
				if(fullconnectcheck(modifynet)==0):#reset
					modifynet[pick][breakpick]=1
					modifynet[breakpick][pick]=1
				broken=1
	return modifynet

# evolve the network to the fewest edges
edgemin=nodes*(nodes-1)/2 + 1
bestnet=[x for x in net]
currentnet=[x for x in net]
for i in range(0, 1000):
	currentnet=netevolve(currentnet)
	edgecurrent=countedge(currentnet)
	if(edgecurrent<edgemin):
		edgemin=copy.deepcopy(edgecurrent)
		print edgemin, edgecurrent, "lower"
		#del bestnet
		bestnet=copy.deepcopy(currentnet)
	else:	
		#del currentnet	
		currentnet=copy.deepcopy(bestnet)
		print edgemin, edgecurrent, "higher"
	# this prints the network with the lowest number of edges
	# it keeps changing even when the number of edges has increased
	DistMatrix =np.array(bestnet)
	G = nx.from_numpy_matrix(DistMatrix)
	nx.draw_graphviz(G)
	plt.draw()
	plt.clf()
	

