#Simulating SIRD model
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import odeint
from matplotlib.widgets import Slider,Button
tld_start = 24
tld_end = 75
def f(z,t):
	fs = -b*z[2]*z[0]*fld(t)/N
	fe = b*z[2]*z[0]*fld(t)/N - s*z[1]
	fi = s*z[1] - c*z[2] - mu*z[2]
	fr = c*z[2]
	fd = mu*z[2]
	return [fs,fe,fi,fr,fd]

def g():
	z = odeint(f,z0,t)
	return z

def fld(t):
	if t<tld_start:
		return 1.
	elif t<tld_end:
		return .5
	else:
		return .02



t_end = 200.
t = np.linspace(0,t_end,1000)
c = .06
s = .1
mu = 0.005
b = .34
r0 = b/(c+mu)
print(r0)
N = 1.2e9
eps = 800
z0 = [N-2*eps,eps,eps,0,0]
capacity = 1e5

z_ret = g()

s = z_ret[:,0]
e = z_ret[:,1]
i = z_ret[:,2]
r = z_ret[:,3]
d = z_ret[:,4]

fig, ax = plt.subplots()
#plt.subplots_adjust(bottom=0.25)
plt.plot(t,[capacity]*len(t),'--',color='black',label="Capacity")
#l1, = plt.plot(t,s,label="S")
#l2, = plt.plot(t,e,label="E")
l3, = plt.plot(t,i,label="I")
#l4, = plt.plot(t,r,label="R")
l5, = plt.plot(t,d,label="D")

#axcolor = 'lightgoldenrodyellow'
#axr0 = plt.axes([0.1,0.1,0.8,0.03], facecolor=axcolor)
#res = plt.axes([0.75,0.03,0.1,0.05],facecolor=axcolor)
#bures = Button(res,'Reset',color=axcolor,hovercolor='0.975')
#sr0 = Slider(axr0,'R\N{SUBSCRIPT ZERO}',1,10,valinit=r0_init,valstep=0.1)

def update_slider(val):
	z_rett = g(val)
	#l1.set_ydata(z_rett[:,0])
	#l2.set_ydata(z_rett[:,1])
	l3.set_ydata(z_rett[:,2])
	#l4.set_ydata(z_rett[:,3])
	l5.set_ydata(z_rett[:,4])
	fig.canvas.draw_idle()

def reset_slider(event):
	sr0.reset()

#sr0.on_changed(update_slider)
#bures.on_clicked(reset_slider)

ax.legend()
ax.set_xlabel("Time")
ax.set_ylabel("States")
fig.suptitle("SIERD Model")
plt.show()
