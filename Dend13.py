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

#Get the number of population, which is equal to the number of rows in a network.
npop=len(net)

print "The number of nodes in the network: %i" % npop

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

	print "The number of nodes with three edges: %i" % threecount

	totedge=(sum(edgesum)/2)
	edges=[] #Place-holder for list of all edges.
	bridges=[] #Place-holder for list of all bridge edges.
	nontermbridge=[] #Place-holder list for non-terminal bridge edges.
	nontermbnodes=[] #Place-holder list for non-terminal nodes connected tobridges.

	#Finds bridges in network by breaking connections and then checking connectivity of network, then checks if nodes and edges are non-terminal.
	for i in range(0,npop):
		for j in range(0,npop):
			netp=copy.deepcopy(net)
			if i!=j and netp[i][j]==netp[j][i]==1:
				edges.append(1)
				netp[i][j]=netp[j][i]=0
				check=fullconnectcheck(netp)
				if check==0:
					bridges.append(1)
					if sum(net[i])>=2:	
						nontermbridge.append(sum(net[i]))
						nontermbnodes.append(i)
				else:
					bridges.append(0)	
	

	#Gives the total number of non-terminal bridge edges.
	nontermbridge=len(nontermbridge)/2

	def unique(seq):
		checked=[]
		for e in seq:
			if e not in checked:
				checked.append(e)
		return checked


	nontermbnodes=unique(nontermbnodes)

	#Makes a list of non-terminal edges and checks if they are connected to each other.
	bridgeconnect=[]
	threebridgeconnect=[]
	for i in nontermbnodes:
		for j in nontermbnodes:
			if i>=0 and j>=0 and i!=j and j>i:
				if net[i][j]==net[j][i]==1:
					bridgeconnect.append(i+j)
					if sum(net[i])==3:
						threebridgeconnect.append(i)


				
	print "Then total number of edges in the matrix: %i" % totedge

	totbridge=sum(bridges)/2
	print "The total number of bridges in the network: %i" % totbridge


	#Sums the total number of non-terminal edges.
	nontbedge=float(len(unique(bridgeconnect)))

	print "The number of non-terminal bridge edges in the network: %i" % nontbedge

	Totnontbridgeflankthree=float(len(unique(threebridgeconnect)))

	print "The number of non-terminal bridge edges in the network that flank nodes with three edges: %i" % Totnontbridgeflankthree

	if nontbedge!=float(0):
		dend = Totnontbridgeflankthree/nontbedge
		print "The dendrisity value of the matrix is: %s" % dend
	else:
		print "The dendrisity value of the matrix is: 0.0"


dend(net)



