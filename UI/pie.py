from pylab import *
from matplotlib import cm

# make a square figure and axes
figure(1, figsize=(13, 6))
ax = axes([0.1, 0.1, 0.8, 0.8])
labelList = []
fracList = []

cs=cm.Set1(np.arange(40)/40.)
setup	= sys.argv[1]

f = open("Results/" + setup + "_resumo.csv", 'r')
lines = f.readlines()
f.close()

for index, line in enumerate(lines):
    if index >= 2:
    	lineSplit = line.split("\t")
    	labelList.append(lineSplit[0])
    	fracList.append(float(lineSplit[2]))

explode=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
pie(fracList, explode=explode, labels=labelList, autopct='%1.1f%%', shadow=True, colors=cs)
title('Memory Access Results', bbox={'facecolor':'0.8', 'pad':10})

gca().set_aspect('1')
show()
