#Stochastic simulation of covid 19

#Tasks:
#Introduce color legend for each state in the plot
#Define cluster points and/or discrete villages

import numpy as np 
import matplotlib.pyplot as plt

#Initial configuration - maybe include cluster points?
def initialize():
	N_pop = 0
	for i in range(size):
		for j in range(size):
			r = np.random.random()
			if r < x_pop:
				if r < x_inf:
					tiles[i,j] = 3
				else:
					tiles[i,j] = 1
				
				N_pop += 1	
	return N_pop

def findI(ptr):
	a = ptr[0]
	b = ptr[1]
	eyes = np.array([a+i for i in range(-e_rad,e_rad+1)])%size
	jays = np.array([b+i for i in range(-e_rad,e_rad+1)])%size

	for i in eyes:
		for j in jays:
			if tiles[i,j] == I:
				return True
	return False	

def count_states():
	count = np.zeros(6,dtype='int')
	for i in range(size):
		for j in range(size):
			count[tiles[i,j]] += 1

	return count	

def randmov():
	for j in range(size):
		for k in range(size):
			r = np.random.random()
			if tiles[j,k] == 0 or tiles[j,k] == D:
				continue
			#Rules - movement
			if r < p_move:
				while True:
					#print("stuck")
					p_xd,p_yd = np.random.random(2)
					dx = int(lam*np.log(1/(lam*p_xd)))
					dy = int(lam*np.log(1/(lam*p_yd)))
					new_j = (j+(-1)**np.random.randint(1,3)*dx)%size
					new_k = (k+(-1)**np.random.randint(1,3)*dy)%size
					#If isEmpty - move there and break, else, try again.
					if tiles[new_j,new_k] == 0:
						tiles[new_j,new_k] = tiles[j,k]
						tiles[j,k] = 0
						if tiles[j,k] == E:
							ndays_exp[new_j,new_k] = ndays_exp[j,k]
							ndays_exp[j,k] = 0
						break		

def infect():
	new_tiles = np.zeros([size,size],dtype='int')
	new_inf = 0
	new_rec = 0
	for j in range(size):
		for k in range(size):
			#Rules - infection
			state = tiles[j,k]
			r = np.random.random()
			new_tiles[j,k] = state
			
			if state == S:
				if findI((j,k)) and r < p_se:
					new_tiles[j,k] = E

			if state == E:
				if r < p_ei:
					new_tiles[j,k] = I
					new_inf += 1
					ndays_exp[j,k] = 0
				else:
					ndays_exp[j,k] += 1

				if ndays_exp[j,k] >= gest_period:
					new_tiles[j,k] = S
					ndays_exp[j,k] = 0

			if state == I:
				if r < p_id:
					new_tiles[j,k] = D
				if r > p_id and r < (p_id+p_ir):
					new_tiles[j,k] = R
					new_rec += 1

	return new_tiles, new_inf, new_rec

#Square tiles
size = 500
tiles = np.zeros([size,size],dtype='int')

x_pop = .1		#fraction of population of the town
e_rad = 5		#Exposure radius - distance b/w S and I for S to turn into E

x_inf = .0001		#Fraction of population infected (initial)

S,E,I,R,D = 1,2,3,4,5

p_se = .4		#Prob to go from S to E once in the proximity of I

p_ei = .3		#Prob to go from E to I

p_id = .0043		#Prob of going from I to D
p_ir = .7		#Prob of going from I to R

#Movement probabilities - movement occurs at the end of a generation
p_move = .05			#Probability of movement initiation
#Distance of movement exponentially decreases
lam = 10	#Average distance travelled

N_pop = initialize()
Ntrials = 500

l = plt.imshow(tiles,interpolation='none')
#Introduce a colour legend for each status
plt.title("Covid 19 stochastic")
ndays_exp = np.zeros([size,size],dtype='int')
gest_period = 14
c_dead = np.zeros(Ntrials,dtype='int')
c_inf = np.zeros(Ntrials,dtype='int')
c_rec = np.zeros(Ntrials,dtype='int')
c_cumrec = np.zeros(Ntrials,dtype='int')
for i in range(Ntrials):
	arr = count_states()
	if arr[E] == 0 and arr[I] == 0:
		break
	#Infection stage
	new_tiles,new_inf,new_rec = infect()
	l.set_data(new_tiles)
	tiles = new_tiles[:,:]
	plt.pause(.1)
	#Random movement stage
	randmov()
	
	#Update plots
	l.set_data(tiles)
	#c_dead[i] = arr[D]
	#c_inf[i] = new_inf
	#c_cumrec[i] = sum(c_rec) + new_rec
	#c_rec[i] = new_rec	
	#plt.plot(range(i),c_inf[:i],color='red',label='Infected')
	#plt.plot(range(i),c_rec[:i],color='blue',label='Recovered')
	#plt.plot(range(i),c_cumrec[:i],color='black',label='Cumulative Recovered')
	#if i == 0:
	#	plt.legend()	
	plt.pause(.1)


plt.show()
