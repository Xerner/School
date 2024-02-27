# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 13:50:50 2021

@author: AndersenB
"""

import random
import matplotlib.pyplot as plt
import numpy as np

def L1(w0,w1,xList,yList):
    loss = 0
    for i in range(len(xList)):
        loss = loss + abs(w0+w1*xList[i] - yList[i])
    return loss/len(xList)

def L1DerivW0(w0,w1,x,y):
    if w0+w1*x-y == 0:
        return 1
    else:
        return ((w0+w1*x - y)/abs(w0+w1*x - y))

def L1DerivW1(w0,w1,x,y):
    if w0+w1*x-y == 0:
        return 1
    else:
        return (x*(w0+w1*x-y)/abs(w0+w1*x-y))

def L2(w0,w1,xList,yList):
    loss = 0
    for i in range(len(xList)):
        loss = (w0+w1*xList[i]-yList[i])**2
    return loss/len(xList)

def L2DerivW0(w0,w1,x,y):
    return 2*(w0+w1*x-y)

def L2DerivW1(w0,w1,x,y):
    return 2*x*(w0+w1*x-y)

def graphLine(w0,w1,color):
    linex = np.linspace(0,100,2)
    liney = w0+w1*linex
    plt.plot(linex,liney,color,label = 'L1')



#********************MakeGraph*****************
random.seed(10)
X= []
Y= []
for i in range(1,50):
    X.append(i*2+random.random())
    Y.append(i*2+random.randint(-2,2))

# plot base points plt.pyplot() 
plt.figure()
plt.plot(X,Y, 'go')
plt.title('Plot Pre Outliers')
# axis labeling
plt.xlabel('x')
plt.ylabel('y')


print("Analysis of L1 vs L2")
print("pre outliers added line of best fit L1 and L2:")
#***************Line Of best Fit****************
#linear model y = mx + b
w0 = 0
w1 = 0
n = .00077
for i in range(len(X)):
    w0 = w0 - n*L1DerivW0(w0,w1,X[i],Y[i])
    w1 = w1 - n*L1DerivW1(w0,w1,X[i],Y[i])

print("L1 final w0:", w0 , " w1:" , w1)
print("loss of L1", L1(w0,w1,X,Y))
    
graphLine(w0,w1,'-b')
    
    
w0 = 0
w1 = 0
n = .00005
for i in range(len(X)):
    w0 = w0 - n*L2DerivW0(w0,w1,X[i],Y[i])
    w1 = w1 - n*L2DerivW1(w0,w1,X[i],Y[i])
print("L2 final w0:", w0 , " w1:" , w1)
print("loss of L2", L2(w0,w1,X,Y))
graphLine(w0,w1,'-r')






#**********Post outliers*****************************************************
#add outliers
X.append(2)
Y.append(40)
X.append(80)
Y.append(2)
X.append(50)
Y.append(100)
X.append(40)
Y.append(10)

plt.figure()
plt.plot(X,Y, 'go')
plt.title('Plot Post Outliers')
# axis labeling
plt.xlabel('x')
plt.ylabel('y')

print("\n\nPost outliers added line of best fit L1 and L2:")
#***************Line Of best Fit****************
#linear model y = mx + b
w0 = 0
w1 = 0
n = .00077
for i in range(len(X)):
    w0 = w0 - n*L1DerivW0(w0,w1,X[i],Y[i])
    w1 = w1 - n*L1DerivW1(w0,w1,X[i],Y[i])

print("L1 final w0:", w0 , " w1:" , w1)
print("loss of L1", L1(w0,w1,X,Y))
    
graphLine(w0,w1,'-b')
plt.show()
    
w0 = 0
w1 = 0
n = .00005
for i in range(len(X)):
    w0 = w0 - n*L2DerivW0(w0,w1,X[i],Y[i])
    w1 = w1 - n*L2DerivW1(w0,w1,X[i],Y[i])
print("L2 final w0:", w0 , " w1:" , w1)
print("loss of L2", L2(w0,w1,X,Y))
graphLine(w0,w1,'-r')
print("blue line = L1 and red line = L2")
