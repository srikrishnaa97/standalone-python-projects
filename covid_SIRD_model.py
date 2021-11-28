#Simulating SIRD model
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import odeint
from matplotlib.widgets import Slider,Button

def f(z,t,b):
	fs = -b*z[1]*z[0]/N
	fi = b*z[1]*z[0]/N - c*z[1] - mu*z[1]
	fr = c*z[1]
	fd = mu*z[1]
	return [fs,fi,fr,fd]

def g(r0=2.7):
	b = r0*(c+mu)
	z = odeint(f,z0,t,args=(b,))
	return z

r0_init = 2.7
t_end = 30.
t = np.linspace(0,t_end,1000)
c = 1.
mu = 0.1
N = 1e6
eps = 1
z0 = [N-eps,eps,0,0]
capacity = 1e5

z_ret = g()

s = z_ret[:,0]
i = z_ret[:,1]
r = z_ret[:,2]
d = z_ret[:,3]

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
plt.plot(t,[capacity]*len(t),'--',color='black',label="Capacity")
l1, = plt.plot(t,s,label="S")
l2, = plt.plot(t,i,label="I")
l3, = plt.plot(t,r,label="R")
l4, = plt.plot(t,d,label="D")

axcolor = 'lightgoldenrodyellow'
axr0 = plt.axes([0.1,0.1,0.8,0.03], facecolor=axcolor)
res = plt.axes([0.75,0.03,0.1,0.05],facecolor=axcolor)
bures = Button(res,'Reset',color=axcolor,hovercolor='0.975')
sr0 = Slider(axr0,'R\N{SUBSCRIPT ZERO}',1,10,valinit=r0_init,valstep=0.1)

def update_slider(val):
	z_rett = g(val)
	l1.set_ydata(z_rett[:,0])
	l2.set_ydata(z_rett[:,1])
	l3.set_ydata(z_rett[:,2])
	l4.set_ydata(z_rett[:,3])
	fig.canvas.draw_idle()

def reset_slider(event):
	sr0.reset()

sr0.on_changed(update_slider)
bures.on_clicked(reset_slider)

ax.legend()
ax.set_xlabel("Time")
ax.set_ylabel("States")
fig.suptitle("SIRD Model")
plt.show()
