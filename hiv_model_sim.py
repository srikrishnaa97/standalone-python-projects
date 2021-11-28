#Simulating HIV
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import odeint

def f(z,t):
	fh = kr1 - kr2*z[0] - kr3*z[0]*z[2]
	fi = kr3*z[0]*z[2] - kr4*z[1]
	fv = -kr3*z[0]*z[2] - kr5*z[2] + kr6*z[1]
	return [fh,fi,fv]

kr1 = 1e5	#New healthy cells per year
kr2 = .1	#death rate of healthy cells
kr3 = 2e-7	#Healthy cells converting to infected cells
kr4 = .5	#death rate of infected cells
kr5 = 5		#death rate of the virus
kr6 = 100	#production of virus by infected cells

t_end = 15
t = np.linspace(0,t_end,1000)
h0 = 1e6
i0 = 0
v0 = 100
z0 = [h0,i0,v0]

z = odeint(f,z0,t)
h = np.array(z[:,0])
i = np.array(z[:,1])
v = np.array(z[:,2])

plt.plot(t,h,label="H")
plt.plot(t,i,label="I")
plt.plot(t,v,label="V")
plt.ylim(bottom=10,top=1e8)
plt.yscale("log")
plt.title("Simulating HIV model")
plt.ylabel("States (log)")
plt.xlabel("Time (years)")
plt.legend()
plt.show()