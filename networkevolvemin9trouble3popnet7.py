# Evolve a fully connected network to have a minimum number of edges
import time
import copy
import random
#random.seed(1234)
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
plt.ion()


#w = 0.99 # heterozygote fitness relative to homozygotes
#m=0.0 # initial migration rate
#inc=0.1 # initial migration rate increment

# number of nodes in the network
nodes = 6 

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



def pnextcalc(w,m,freq,popnet,immi,errorflag):
	#print freq
	# calculate avereage allele frequency after migration
	
	pave=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

	# >>>> something is wrong here, should not go >1 <<<<<<

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

	#for i in range(0, nodes):
	#	if(pave[i]>1):
	#		pave[i]=1
	#		print "ERROR p>1", m
	#		print pave
	#	elif(pave[i]<0):
	#		pave[i]=0
	#		print "ERROR p<0", m

	#if(errorflag):
		#print "freq", freq
		#print "pave", pave

	
	# calculate average fitness
	wbar=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in range(0, nodes):
		wbar[i] = pave[i]*pave[i] + 2*w*pave[i]*(1-pave[i]) + (1-pave[i])*(1-pave[i])
	#print "wbar ", wbar
	#for i in range(0, nodes):
	#	if(pave[i]>=1):
	#		print wbar
	#	elif(pave[i]<=0):
	#		print wbar
	
	# update frequencies with selection
	pnext=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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

	## store new values
	#for i in range(0, nodes):
	#	freq[i]=pnext[i]

	# print pnext	

	return diff


# calculate distance in allele frequency between popualtions
def dist(freq):
	distance=0
	for i in range(0, nodes):
		for j in range(0, nodes):
			distance=distance+abs(freq[i]-freq[j])
	return distance



tro = open('troubleshoot.txt', 'w')


mcritmax=0
mcritcurrent=0
# evolve the network to the fewest edges
edgemin=nodes*(nodes-1)/2 + 1
bestnet=[x for x in net]
currentnet=[x for x in net]
#initialize critical migration rates
	
DistMatrix =np.array(bestnet)
G = nx.from_numpy_matrix(DistMatrix)
pos=nx.graphviz_layout(G)
nx.draw_networkx_nodes(G,pos,
                       nodelist=[0,1,2],
                       node_color='r',
                       node_size=500,
                   alpha=0.8,labels=None,node_alpha=0.1)
nx.draw_networkx_nodes(G,pos,
                       nodelist=[3,4,5],
                       node_color='b',
                       node_size=500,
                   alpha=0.8,labels=None,node_alpha=0.1)
nx.draw_graphviz(G,labels=None,node_alpha=0.1)
plt.draw()
plt.clf()

inc=0.1
m=0.0
w = 0.95	
errorflag=0
immi=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0, nodes):
	for j in range(0, nodes):
		immi[i]=immi[i]+currentnet[i][j]
	#if(i==4):
	#	errorflag=1
for x in range(0,4):
	distance=1
		#for j in range(0,1000):
	while(distance>0.0001):
			#print "up", m
		difference=1
			#freq = initfreq[:]
			#freq=copy.deepcopy(initfreq)
		#freq = [1,0.99,1,1.0,1.0,1,1,0.02,0.01,0.0,0,0,0,0] # 14
		freq = [1,0.99,1,0.02,0.01,0.0] # 6

			#print "freq ", freq
			#print freq
			#j=0
			#for k in range(0,10):
		while(difference>0.000000001):
			prefreq=copy.deepcopy(freq)
			freq=pnextcalc(w,m,freq,currentnet,immi,errorflag)
			difference=diff(prefreq,freq)
			currenttime=time.time()
				#if(currenttime-starttime > 10):
				#	break
				#if(errorflag):
					#print currentnet
					#if(j%10 == 0):
						#line=(freq,"\n")
						#tro.write(str(line))
				#j=j+1
				#print difference
				#print freq
		distance=dist(freq)
			#print "distance", distance
		m=m+inc

			#if(currenttime-starttime > 10):
			#	break

				#print freq
		#if(freq[0]>0.5):
		#	errorflag=1	
		#if(m<0):
		#	errorflag=1	
		#if(m>0.5):
		#	m=0.0
		#	errorflag=1
		#else:
	m=m-2*inc
		#print "down", m
	print m
	inc=inc/10
		#if(errorflag):
			#print currentnet
			#print freq
print m

	#if(m>0.5):
print currentnet
	#print initfreq
	#print "freq ", freq
	#print "immi ", immi

mcritcurrent=copy.deepcopy(m)
mcritmax=copy.deepcopy(mcritcurrent)

lastupdate=0
s=0
while(True):
#for i in range(0, 100):
	print "step ", s, " last update ", lastupdate
	s=s+1
	w = 0.95	
	#if(i==4):
	#	print "w ", w
	changesteps = random.randrange(0, 100)
	print "changes ", changesteps
	currentnet=netevolve(currentnet)

	if(changesteps>25):
		currentnet=netevolve(currentnet) # allow two step changes (break and reattach)
	if(changesteps>50):
		currentnet=netevolve(currentnet)
	if(changesteps>75):
		currentnet=netevolve(currentnet)
	if(changesteps>90):
		currentnet=netevolve(currentnet)
	if(changesteps>95):
		currentnet=netevolve(currentnet)
	if(changesteps>98):
		currentnet=netevolve(currentnet)

	edgecurrent=countedge(currentnet)

	# count number of inputs for each population
	immi=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in range(0, nodes):
		for j in range(0, nodes):
			immi[i]=immi[i]+currentnet[i][j]


	# estimate critical migration rate
	inc=0.1
	m=0.0
	starttime=time.time()
	errorflag=0
	#if(i==4):
	#	errorflag=1
	for x in range(0,4):
		distance=1
		#for j in range(0,1000):
		while(distance>0.0001):
			#print "up", m
			difference=1
			#freq = initfreq[:]
			#freq=copy.deepcopy(initfreq)
			#freq = [1,0.99,1,1.0,1.0,1,1,0.02,0.01,0.0,0,0,0,0] # 14
			freq = [1,0.99,1,0.02,0.01,0.0] # 6
			
			#print "freq ", freq
			#print freq
			#j=0
			#for k in range(0,10):
			while(difference>0.000000001):
				prefreq=copy.deepcopy(freq)
				freq=pnextcalc(w,m,freq,currentnet,immi,errorflag)
				difference=diff(prefreq,freq)
				currenttime=time.time()
				#if(currenttime-starttime > 10):
				#	break
				#if(errorflag):
					#print currentnet
					#if(j%10 == 0):
						#line=(freq,"\n")
						#tro.write(str(line))
				#j=j+1
				#print difference
				#print freq
			distance=dist(freq)
			#print "distance", distance
			m=m+inc
			currenttime=time.time()
			#if(currenttime-starttime > 10):
			#	break
			if(errorflag):
				tro.write(str(currentnet))
				#print freq
		#if(freq[0]>0.5):
		#	errorflag=1	
		#if(m<0):
		#	errorflag=1	
		#if(m>0.5):
		#	m=0.0
		#	errorflag=1
		#else:
		m=m-2*inc
		#print "down", m
		print m
		inc=inc/10
		#if(errorflag):
			#print currentnet
			#print freq
	print m

	#if(m>0.5):
	print currentnet
	#print initfreq
	#print "freq ", freq
	#print "immi ", immi

	mcritcurrent=copy.deepcopy(m)

	if(mcritcurrent>=mcritmax):
		mcritmax=copy.deepcopy(mcritcurrent)
		print mcritmax, mcritcurrent, "higher"
		#del bestnet
		bestnet=copy.deepcopy(currentnet)
		lastupdate=s
	else:	
		#del currentnet	
		currentnet=copy.deepcopy(bestnet)
		print mcritmax, mcritcurrent, "lower"

	#DistMatrix2 =np.array(currentnet)
	#G2 = nx.from_numpy_matrix(DistMatrix2)
	#nx.draw_graphviz(G2)
	#plt.draw()
	#plt.clf()


	#if(edgecurrent<=edgemin):
	#	edgemin=copy.deepcopy(edgecurrent)
	#	print edgemin, edgecurrent, "lower"
	#	#del bestnet
	#	bestnet=copy.deepcopy(currentnet)
	#else:	
	#	#del currentnet	
	#	currentnet=copy.deepcopy(bestnet)
	#	print edgemin, edgecurrent, "higher"
	# this prints the network with the lowest number of edges
	# it keeps changing even when the number of edges has increased
	DistMatrix =np.array(bestnet)
	G = nx.from_numpy_matrix(DistMatrix)
	pos=nx.graphviz_layout(G)
	nx.draw_networkx_nodes(G,pos,
                       nodelist=[0,1,2],
                       node_color='r',
                       node_size=500,
                   alpha=0.8,labels=None,node_alpha=0.1)
	nx.draw_networkx_nodes(G,pos,
                       nodelist=[3,4,5],
                       node_color='b',
                       node_size=500,
                   alpha=0.8,labels=None,node_alpha=0.1)
	nx.draw_graphviz(G,labels=None,node_alpha=0.1)
	plt.draw()
	plt.clf()

	#if(errorflag):
	#	break
plt.savefig("network6w95m.png") # save as png	

