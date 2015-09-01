# Evolve a fully connected network 
# of popualtions have higher stability
# of an underdominant polymorphism

import time
import copy
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
plt.ion()


# number of nodes in the network
nodes = 6 # just have to change this

plotnet = 1 # 1 if plot network, 0 is no figure



outfile = open("bestnetoutput.txt", "wb")

w = 0.0 # heterozygote fitness relative to homozygotes

freq = [0 for x in range(nodes)]

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



mcritmax=0
mcritcurrent=0
edgemin=nodes*(nodes-1)/2 + 1
bestnet=[x for x in net]
currentnet=[x for x in net]
if(plotnet):
	DistMatrix =np.array(bestnet)
	G = nx.from_numpy_matrix(DistMatrix)
	pos=nx.graphviz_layout(G)
	nx.draw_graphviz(G,labels=None,node_alpha=0.1)
	plt.draw()
	plt.clf()

inc=0.1
m=0.0	
errorflag=0
immi = [0 for x in range(nodes)]
for i in range(0, nodes):
	for j in range(0, nodes):
		immi[i]=immi[i]+currentnet[i][j]
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

		while(difference>0.000000001):
			prefreq=copy.deepcopy(freq)
			freq=pnextcalc(w,m,freq,currentnet,immi)
			difference=diff(prefreq,freq)
			currenttime=time.time()
		distance=dist(freq)
		m=m+inc
	m=m-2*inc
	if(m == 0.0):
		digitplaces=digitplaces+1
	if(digitplacecount==digitplaces):
		break
	print m
	inc=inc/10
print m
print currentnet

mcritcurrent=copy.deepcopy(m)
mcritmax=copy.deepcopy(mcritcurrent)

lasthigher=0
lastaccept=0
s=0
#while(True):
for i in range(0, 100):
	print "step ", s, " last accept ", lastaccept, " last improve ", lasthigher
	s=s+1
	changesteps = random.randrange(0, 100)
	currentnet=netevolve(currentnet)

	if(changesteps>50):
		currentnet=netevolve(currentnet) 
	if(changesteps>75):# allow two step changes (break and reattach)
		currentnet=netevolve(currentnet)
	if(changesteps>90):
		currentnet=netevolve(currentnet)
	if(changesteps>95):
		currentnet=netevolve(currentnet)
	if(changesteps>97):
		currentnet=netevolve(currentnet)
	if(changesteps>98):
		currentnet=netevolve(currentnet)

	edgecurrent=countedge(currentnet)

	# count number of inputs for each population
	immi = [0 for x in range(nodes)]
	for i in range(0, nodes):
		for j in range(0, nodes):
			immi[i]=immi[i]+currentnet[i][j]


	# estimate critical migration rate
	inc=0.1
	m=0.0
	errorflag=0
	digitplaces=3
	digitplacecount=0
	while(True):
		digitplacecount=digitplacecount+1
		distance=1
		while(distance>0.0001):
			difference=1

			#initialize frequencies
			for z in range(0, nodes):
				freq[z]=0+random.random()/50
			for z in range(0, nodes/2):
				freq[z]=1-random.random()/50
			
			while(difference>0.000000001):
				prefreq=copy.deepcopy(freq)
				freq=pnextcalc(w,m,freq,currentnet,immi)
				difference=diff(prefreq,freq)

			distance=dist(freq)
			m=m+inc
		m=m-2*inc
		if(m == 0.0):
			digitplaces=digitplaces+1
		if(digitplacecount==digitplaces):
			break
		print m
		inc=inc/10
	print m
	print currentnet

	mcritcurrent=copy.deepcopy(m)
	
	randpick=random.random()
	if(mcritcurrent>mcritmax):
		mcritmax=copy.deepcopy(mcritcurrent)
		print "m: ", mcritmax, mcritcurrent, "higher"
		bestnet=copy.deepcopy(currentnet)
		lasthigher=s
		outfile.write(str(bestnet)+"\n")
		outfile.write(str(mcritmax)+"\n")
		outfile.write(str(w)+"\n")
		outfile.write(str(nodes)+"\n")
	elif(randpick<(mcritcurrent/mcritmax)):
		print "m: ", mcritmax, mcritcurrent, "accept"
		lastaccept=s
	else:	
		currentnet=copy.deepcopy(bestnet)
		print "m: ", mcritmax, mcritcurrent, "lower"
	print "w: ", w
	if(m>0.1):
		w=w+(1-w)/10
		#if this is done the mrcitmax has to be reset
		inc=0.1
		m=0.0
		errorflag=0
		digitplaces=3
		digitplacecount=0
		while(True):
			digitplacecount=digitplacecount+1
			distance=1
			while(distance>0.0001):
				difference=1

				#initialize frequencies
				for z in range(0, nodes):
					freq[z]=0+random.random()/50
				for z in range(0, nodes/2):
					freq[z]=1-random.random()/50
			
				while(difference>0.000000001):
					prefreq=copy.deepcopy(freq)
					freq=pnextcalc(w,m,freq,bestnet,immi)
					difference=diff(prefreq,freq)
				distance=dist(freq)
				m=m+inc

			m=m-2*inc
			if(m == 0.0):
				digitplaces=digitplaces+1
			if(digitplacecount==digitplaces):
				break
			print m
			inc=inc/10
		mcritmax=copy.deepcopy(m)

	if(plotnet):
		DistMatrix =np.array(currentnet)
		G = nx.from_numpy_matrix(DistMatrix)
		pos=nx.graphviz_layout(G)
		nx.draw_graphviz(G,labels=None,node_alpha=0.1)
		plt.draw()
		plt.clf()


