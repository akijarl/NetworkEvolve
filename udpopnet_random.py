# generate random fully connected networks
# and evaluate their properties

import time
import copy
import random
import networkx as nx
import numpy as np
#import matplotlib.pyplot as plt
#plt.ion()
plotnet = 1 # 1 if plot network, 0 is no figure

outfile = open("randomnetoutput.txt", "wb")
outfile.write("Node"+"\t"+ "Edges"+"\t"+"Mcrit"+"\t"+"Var"+"\t"+"Eff"+"\t"+"Var/Edge"+"\t"+"MaxDiam"+"\t"+"Dend"+"\t"+"Terminal"+"\t"+"Even"+"\t"+"V/E"+"\t"+"Net"+"\n")

nodes = 10
edges = 15

npop=copy.deepcopy(nodes)
edgerange=1
noderange=1
if(noderange):
	# range of nodes in the network
	minnode = 2
	maxnode = 20

#nodes = 8 # just have to change this

replicates = 100

w = 0.5 # heterozygote fitness relative to homozygotes

def linearness(net, npop):
	# special case for a network of 2 populations
	if(npop == 2):
		return 1
	else:
		# determine the distance between all popualtion pairs
		maxdiameter=0
		for i in range(1, npop):
			link = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			linkcopy = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			for k in range(1, npop):
				for j in range(0, npop):
					if (i != j):
						if(link[j]==0):
							if(net[i][j]==1):
								linkcopy[j]=k
						else:
							for l in range(0, npop):
								if (i != l):
									if(link[l]==0):
										if(net[j][l]==1):
											linkcopy[l]=k
				link = copy.deepcopy(linkcopy)
				#print link
			for j in range(0, npop):
				if(link[j]>maxdiameter):
					maxdiameter=link[j]
		#print "diameter: ", maxdiameter
		# alternative could return diameter by uncommenting below
		#return maxdiameter
		#print "linearness: ", (float(maxdiameter)-1)/(float(npop)-2)
		return ((float(maxdiameter)-1)/(float(npop)-2))


def eff(net, npop):
	# special case for a network of 2 populations
	if(npop == 2):
		return 1
	else:
		# determine the distance between all popualtion pairs
		invert=[]
		for i in range(1, npop):
			link = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			linkcopy = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			for k in range(1, npop):
				for j in range(0, npop):
					if (i != j):
						if(link[j]==0):
							if(net[i][j]==1):
								linkcopy[j]=k
						else:
							for l in range(0, npop):
								if (i != l):
									if(link[l]==0):
										if(net[j][l]==1):
											linkcopy[l]=k
				link = copy.deepcopy(linkcopy)
		for m in range(len(link)):
			if link[m]!=0:
				invert.append(1/float(link[m]))
		return float(sum(invert))/(float(npop)*(npop-1))
		
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

#Function for calculating dendrisity value.
def dend(net):
	#Makes a list of the number of edges each node in the network has.
	edgesum=[]
	for i in net:
		edgesum.append(sum(i))
	#print "The number of edges at each node: %s" % edgesum
	#Makes a list of the number of nodes that have three edges.
	threecount=0
	for i in edgesum:
		if i==3:
			threecount=threecount+1
	#print "The number of nodes with three edges: %i" % threecount
	edges=[] #Place-holder for list of all edges.
	bridges=[] #Place-holder for list of all bridge edges.
	nontermnodebridges=[] #Place-holder list for non-terminal bridge edges.
	nontermbnodes=[] #Place-holder list for non-terminal nodes connected tobridges.
	#Finds bridges in network by breaking connections and then checking connectivity of network, then checks if nodes and edges are non-terminal.
	for i in range(0,nodes):
		for j in range(0,nodes):
			netp=copy.deepcopy(net)
			if i!=j and netp[i][j]==netp[j][i]==1:
				edges.append(1)
				netp[i][j]=netp[j][i]=0
				check=fullconnectcheck(netp)
				if check==0:
					bridges.append(1)
					if sum(net[i])>=2:	
						nontermnodebridges.append(str(i)+str(j))
						nontermbnodes.append(i)
				else:
					bridges.append(0)	
	#Gives the total number of non-terminal bridge edges.
	#nontermbridge=len(nontermbridge)/2
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
					bridgeconnect.append(str(i)+str(j))
					if sum(net[i])==3:
						threebridgeconnect.append(i)
	totedge=(sum(edgesum)/2)
	#print "Then total number of edges in the matrix: %i" % totedge
	totbridge=sum(bridges)/2
	#print "The total number of bridges in the network: %i" % totbridge
	#Sums the total number of non-terminal edges.
	#nontbedge=float(len(unique(bridgeconnect)))
	#Checks if the bridges involving non-terminal nodes are to another non-terminal node.
	nontermbridgeconnect=0
	for i in range(0,len(bridgeconnect)):
		if bridgeconnect[i] in nontermnodebridges:
			nontermbridgeconnect+=1	
	#print "The number of non-terminal bridge edges in the network: %i" % nontermbridgeconnect
	Totnontbridgeflankthree=float(len(unique(threebridgeconnect)))
	#print "The number of non-terminal nodes in the network that flank nodes with three edges: %i" % Totnontbridgeflankthree
	if nontermbridgeconnect!=float(0):
		dend = Totnontbridgeflankthree/float(len(nontermbnodes))
	else: 
		dend="0"
	return dend

def pnextcalc(w,m,freq,popnet,immi):
	# calculate avereage allele frequency after migration
	pave = [0 for x in range(nodes)]
	for i in range(0, nodes):
		for j in range(0, nodes):
			if i == j:
				# normalization step if m is too large
				if(immi[i]*m <= 1):
					# p = global freq[j]
					pave[i]=pave[i]+(1-immi[i]*m) * freq[j]
				else:
					pave[i]=0
			elif popnet[i][j] == 1:
				if(immi[i]*m <= 1):
					pave[i] = pave[i] + m * freq[j]
				else:
					pave[i] = pave[i] + m * freq[j] / immi[i]*m
	# calculate average fitness
	wbar = [0 for x in range(nodes)]
	for i in range(0, nodes):
		wbar[i] = pave[i]*pave[i] + 2*w*pave[i]*(1-pave[i]) + (1-pave[i])*(1-pave[i])
	# update frequencies with selection
	pnext = [0 for x in range(nodes)]
	for i in range(0, nodes):
		pnext[i] = (pave[i]*pave[i] + w*pave[i]*(1-pave[i]))/wbar[i]
	# boundry at zero and one
	for i in range(0, nodes):
		if(pnext[i]>1):
			pnext[i]=1
		if(pnext[i]<0):
			pnext[i]=0
	# store new values
	for i in range(0, nodes):
		freq[i]=pnext[i]
	return freq


def diff(freq, pnext):
	# calculate change
	diff=0
	for i in range(0, nodes):
		diff=diff+abs(pnext[i]-freq[i])
	return diff

# calculate distance in allele frequency between popualtions
def dist(freq):
	distance=0
	for i in range(0, nodes):
		for j in range(0, nodes):
			distance=distance+abs(freq[i]-freq[j])
	return distance

def terminalness(net,npop):
	# what fraction of the nodes are terminal nodes
	# these only have one connection in the rows
	term = 0
	for i in range(0, npop):
		rowsum = 0
		for j in range(0, npop):
			rowsum = rowsum + net[i][j]
		if(rowsum == 1):
			term = term + 1
		#print rowsum
		#print term
	return float(term)/float(npop)


for r in range(0, replicates):
	if(noderange):
		nodes = random.randrange(minnode,maxnode+1)
	if(edgerange):
		minedge = nodes-1 # minimum # edges possible
		maxedge = nodes*minedge/2 #maximum # edges possible
		edgepick = random.randrange(minedge,maxedge+1)
		#print edgepick
	else:
		edgepick = edges
	# create networks until fully interconnected
	while(1):
		# initial empty network matrix
		net = [[0 for x in range(nodes)] for x in range(nodes)] 
		# place random edges
		countedge=0
		while(1):
			if(countedge == edgepick): 
				break
			#for i in range(0, edgepick): 
			x = random.randrange(0,nodes)
			y = random.randrange(0,nodes)
			if(x != y): 
				if(net[x][y] == 0): 
					net[x][y]=1
					net[y][x]=1
					countedge=countedge+1
		# evaluate if fully interconnected
		if(fullconnectcheck(net) == 1):
			break
	#print net
	if(plotnet):
		DistMatrix =np.array(net)
		G = nx.from_numpy_matrix(DistMatrix)
		#pos=nx.graphviz_layout(G)
		#nx.draw_graphviz(G,labels=None,node_alpha=0.1)
		#plt.draw()
		#plt.clf()
	# evaluate stability
	freq = [0 for x in range(nodes)]
	inc=0.1
	m=0.0	
	errorflag=0
	immi = [0 for x in range(nodes)]
	for i in range(0, nodes):
		for j in range(0, nodes):
			immi[i]=immi[i]+net[i][j]
	digitplaces=3
	digitplacecount=0
	while(True):
		digitplacecount=digitplacecount+1
		distance=1
		while(distance>0.0001):
			difference=1
			for z in range(0, nodes):
				freq[z]=0+random.random()/50
			for z in range(0, nodes/2):
				freq[z]=1-random.random()/50

			while(difference>0.0000000001):
				prefreq=copy.deepcopy(freq)
				freq=pnextcalc(w,m,freq,net,immi)
				difference=diff(prefreq,freq)
				#currenttime=time.time()
			distance=dist(freq)
			m=m+inc
		m=m-2*inc
		if(m == 0.0):
			digitplaces=digitplaces+1
		if(digitplacecount==digitplaces):
			break
		#print m
		inc=inc/10
	#print m
	#print net
	# calcualte variance in connectivity
	aveconnect = edgepick/nodes
	sumnodeconnect = [0 for x in range(nodes)]
	for i in range(0, nodes):
		for j in range(0, nodes):
			if(net[i][j]):
				sumnodeconnect[i] = sumnodeconnect[i]+1
	varsum=0.0
	for i in range(0, nodes):	
		varsum = varsum + (sumnodeconnect[i] - aveconnect)*(sumnodeconnect[i] - aveconnect)
	variance = varsum / nodes
	# end calcualte variance in connectivity
	# calculate network diameter and average shortest path length?
	# calculate dendrosity
	#bigY = dend(net)	
	#print bigY
	#print "nodes = ", nodes
	#print "edges = ", edgepick
	#print "variance = ", variance
	#print "m* = ", m
	nodeoutput = str(nodes)
	edgeoutput = str(edgepick)
	nodesperedge = str(float(nodes)/float(edgepick))
	veoutput = str(nodesperedge)
	moutput = str(m)
	varoutput = str(variance)
	varianceperedge = str(variance/float(edgepick))
	varedgeoutput = str(varianceperedge)
	lin=linearness(net,nodes)
	linoutput=str(lin)
	#Youtput = str(bigY)
	dendo=dend(net)	
	dendout=str(dendo)
	ter=terminalness(net,nodes)
	teroutput = str(ter)
	effo = eff(net,nodes)
	effoutput = str(effo)
	if(nodes%2 == 0):
		eveness=1
	else:
		eveness=0
	evenoutput = str(eveness)
	netoutput = str(net)
	outfile.write(nodeoutput+"\t"+edgeoutput+"\t"+moutput+"\t"+varoutput+"\t"+effoutput+"\t"+varedgeoutput+"\t"+linoutput+"\t"+dendout+"\t"+teroutput+"\t"+evenoutput+"\t"+veoutput+"\t"+netoutput+"\n")

	print r, " ", nodes, " ", edgepick, " ", m

	#pause until enter
	##q = input("Press Enter to continue...")

exit()


