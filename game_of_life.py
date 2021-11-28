#Conway's Game of Life
import numpy as np 
import matplotlib.pyplot as plt 

#Square tiles
size = 100

#Initial configuration - check the wikipedia page for game of life to change to a desired pattern
def initialize():
	return np.random.randint(0,2,(size,size))

def count_neighbours(ptr):
	a = ptr[0]
	b = ptr[1]
	count = 0
	#Periodic boundary condition - torus
	cols = [(a-1)%size,a,(a+1)%size]
	rows = [(b-1)%size,b,(b+1)%size]
	

	count = np.sum(np.array([[tiles[m,n] for m in cols] for n in rows])) - tiles[a,b]
	return count

tiles = initialize()
Ntrials = 100
l = plt.imshow(tiles,interpolation='none',cmap='gray')
plt.title("Conway's Game of Life")

for i in range(Ntrials):
	new_tiles = np.zeros([size,size],dtype='int')
	for j in range(size):
		for k in range(size):
			#Rules
			nn = count_neighbours((j,k))
			state = tiles[j,k]
			new_tiles[j,k] = state
			if state == 0 and nn == 3:
				new_tiles[j,k] = 1
			if state == 1 and nn < 2:
				new_tiles[j,k] = 0
			if state == 1 and nn > 3:
				new_tiles[j,k] = 0

	#Plotting the updated tiles
	l.set_data(new_tiles)
	tiles = new_tiles[:,:]	
	plt.pause(.1)

plt.show()
