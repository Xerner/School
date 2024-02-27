import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

print("My model is: ax+b")

x = np.arange(100)
y = np.random.randint(0, 100, 100)
y2 = 2*x+4

plt.plot(x,y, 'bo')
plt.plot(x,y2, 'r')
plt.show()