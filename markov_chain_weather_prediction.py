#Markov chain to output probability of next day's weather from previous day's weather
import numpy as np
from numpy.random import rand
import sys

out = 0
if len(sys.argv) == 2:
	out = int(sys.argv[1])
	if out != 0 and out != 1 and out != -1:
		print("-1,0,1 allowed")
		exit()

p_cs = .3                       #Probability that it is cloudy given yesterday was sunny
p_rs = .2                       #Probability that it is rainy given yesterday was sunny
p_ss = 1 - p_cs - p_rs          #Probability that it is sunny given yesterday was sunny

p_sc = .4                       #Probability that it is sunny given yesterday was cloudy
p_rc = .4                       #Probability that it is rainy given yesterday was cloudy
p_cc = 1 - p_rc - p_sc          #Probability that it is cloudy given yesterday was cloudy

p_sr = .2                       #Probability that it is sunny given yesterday was rainy
p_cr = .4                       #Probability that it is cloudy given yesterday was rainy
p_rr = 1 - p_cr - p_sr          #Probability that it is rainy given yesterday was rainy

P = np.array([[p_ss,p_sc,p_sr],[p_cs,p_cc,p_cr],[p_rs,p_rc,p_rr]])

Ndays = 1000
NN = 10000

#1 = sunny; 0 = cloudy; -1 = rainy
weather_dict = {1:'sunny',0:'cloudy',-1:'rainy'}

#Starting with a sunny day = 1, cloudy day = 0, rainy day = -1
init_cond = 0
days = np.ones(NN,dtype='int')*init_cond

for i in range(Ndays):
	for j in range(NN):
		r = rand()
		day = days[j]
		if day == 1 and r < p_cs:
			days[j] = 0
		if day == 1 and r < (p_cs+p_rs) and r > p_cs:
			days[j] = -1
		if day == 0 and r < p_sc:
			days[j] = 1
		if day == 0 and r < (p_sc+p_rc) and r > p_sc:
			days[j] = -1
		if day == -1 and r < p_sr:
			days[j] = 1
		if day == -1 and r < (p_sr+p_cr) and r > p_sr:
			days[j] = 0

	if i%20 == 0:
		print("Chance of %s weather on day %d\t%f"%(weather_dict[out],i,float(np.sum(days==out))/NN))