import time
import random
import copy

fullyconnected20 = [[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
	[1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]]

reverselinear20 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1], 
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

linear20 = [[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
	[1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]]

circle=[[0,1,0,0,0,1],
[1,0,1,0,0,0],
[0,1,0,1,0,0],
[0,0,1,0,1,0],
[0,0,0,1,0,1],
[1,0,0,0,1,0]]

perfecttree=[[0,1,0,0,0,0],
[1,0,1,1,0,0],
[0,1,0,0,0,0],
[0,1,0,0,1,1],
[0,0,0,1,0,0],
[0,0,0,1,0,0]]

Yshape=[[0,1,0,0,0,0],
[1,0,1,0,1,0],
[0,1,0,1,0,0],
[0,0,1,0,0,0],
[0,1,0,0,0,1],
[0,0,0,0,1,0]]

fullconnect=[[0,1,1,1,1,1],
[1,0,1,1,1,1],
[1,1,0,1,1,1],
[1,1,1,0,1,1],
[1,1,1,1,0,1],
[1,1,1,1,1,0]]

twomountbyplain=[[0,1,1,0,0,0],
[1,0,1,0,0,0],
[1,1,0,1,1,0],
[0,0,1,0,1,0],
[0,0,1,1,0,1],
[0,0,0,0,1,0]]

notconnect=[[0,0,1,0,0,0],
[0,0,0,1,1,1],
[1,0,0,0,0,0],
[0,1,0,0,1,1],
[0,1,1,0,0,1],
[0,1,1,0,1,0]]

linear=[[0,1,0,0,0,0],
[1,0,1,0,0,0],
[0,1,0,1,0,0],
[0,0,1,0,1,0],
[0,0,0,1,0,1],
[0,0,0,0,1,0]]

southerncross=[[0,1,0,0,0,0],
[1,0,1,1,1,0],
[0,1,0,0,0,0],
[0,1,0,0,0,0],
[0,1,0,0,0,1],
[0,1,0,0,1,0]]

#Code for assessing the level of dendrisity in a network.
net = reverselinear20 

#Creates a copy of network that is modifiable without affecting the original network.
netp=copy.deepcopy(net)

#Function which checks if a network is fully connected or if it consists of multiple networks.
def fullconnectcheck(net):
	# check if the network is interconnected
	connected = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
	current=0
	for k in range(0, npop): 
		for j in range(0, npop):
			current = j
			if(connected[j] == 1):
				for i in range(0, npop): # walks through and finds connections to first pop
					if(i != current):
						if(net[current][i]==1):
							connected[i]=1
							#print connected
	connectcount=0
	for j in range(0, npop):
		if(connected[j]==1):
			connectcount=connectcount+1
	if(connectcount == npop):
		#print "fully connected"
		return 1
	else: 
		#print "not connected"
		return 0

#Get the number of population, which is equal to the number of rows in a network.
npop=len(net)


#Function for calculating dendrisity value.
def dend(net):
	#Makes a list of the number of edges each node in the network has.
	edgesum=[]
	for i in net:
		edgesum.append(sum(i))

	print "The number of edges at each node: %s" % edgesum

	#Makes a list of the number of nodes that have three edges.
	threecount=0
	for i in edgesum:
		if i==3:
			threecount=threecount+1

	print "The number of nodes with three edges: %s" % threecount

	totedge=(sum(edgesum)/2)
	edges=[] #Place-holder for list of all edges.
	bridges=[] #Place-holder for list of all bridge edges.
	nontermbridge=[-1]*totedge #Place-holder list for non-terminal bridge edges.
	nontermbnodes=[-1]*totedge #Place-holder list for non-terminal nodes connected tobridges.

	#Finds bridges in network by breaking connections and then checking connectivity of network, then checks if nodes and edges are non-terminal.
	for i in range(0,npop):
		for j in range(0,npop):
			netp=copy.deepcopy(net)
			if i!=j and j>i and netp[i][j]==netp[j][i]==1:
				edges.append(1)
				netp[i][j]=netp[j][i]=0
				check=fullconnectcheck(netp)
				if check==0:
					bridges.append(1)
					if sum(net[i])>=2:	
						nontermbridge[i]=(sum(net[i]))
						nontermbnodes[i]=i
				else:
					bridges.append(0) 

	#Final list for non-terminal nodes connected to bridges.
	#nontermbnodes=set(nontermbnodes)
	#nontermbnodes=list(nontermbnodes)

	#Makes a list of all nodes that are non-terminal that have exactly three edges.
	#nontermbnodesthree=[]
	#for k in range(0,len(nontermbridge)):			
	#	if nontermbridge[k]==3:
	#		nontermbnodesthree.append(nontermbnodes[k])

	#Makes a list of non-terminal edges and checks if they are connected to each other.
	bridgeconnect=[]
	threebridgeconnect=[]
	for i in nontermbnodes:
		for j in nontermbnodes:
			if i>=0 and j>=0 and i!=j and j>i:
				if net[i][j]==net[j][i]==1:
					bridgeconnect.append(1)
					if sum(net[i])==3:
						threebridgeconnect.append(1)
					else:
						threebridgeconnect.append(0)
				

	#List of number of bridge edges on the non-terminal nodes.
	#nontbridge=[] 
	#for i in range(0,len(nontermbridge)):
	#	if nontermbridge[i]>0:
	#		nontbridge.append(1)


	totedge=sum(edges)
	print "Then total number of edges in the matrix: %s" % totedge

	totbridge=sum(bridges)
	print "The total number of bridges in the network: %s" % totbridge


	#Sums the total number of non-terminal edges.
	nontbedge=sum(bridgeconnect)

	print "The number of non-terminal bridge edges in the network: %s" % nontbedge

	Totnontbridgeflankthree=sum(threebridgeconnect)

	print "The number of non-terminal bridge edges in the network that flank nodes with three edges: %s" % Totnontbridgeflankthree

	if nontbedge!=float(0):
		dend = float(Totnontbridgeflankthree)/float(nontbedge)
		print "The dendrisity value of the matrix is: %s" % dend
	else:
		print "The dendrisity value of the matrix is: 0.0"


dend(net)



