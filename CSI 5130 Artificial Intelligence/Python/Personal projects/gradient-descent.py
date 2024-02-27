import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pandas.core.construction import array

np.random.seed(42)
# print('Required Libraries:\ttime, numpy, matplotlib')

# algorithm constants
iterations = 1
learningRate = 0.00000001

# data
inputs = pd.read_csv(r'./real-estate-sales.csv')
target = inputs.pop('price')
inputs.drop(inputs.columns[0], axis=1, inplace=True)
# inputs.insert(0,'bias-coef',1)
inputs = inputs.to_numpy()

def gradientDescent(inputs, target):
  coef = np.zeros(inputs.shape[1]+1)
  for k in range(iterations):
    # train parameters
    print('\nIteration ', k,'\n')
    for xi, expected_value in zip(inputs, target):
      prediction = predict(xi, coef)
      print(xi)
      # print(expected_value)
      # print('cost',prediction - expected_value)
      coef[0] = coef[0] - learningRate * (prediction - expected_value) * 1
      coef[1:] = coef[1:] - learningRate * (prediction - expected_value) * xi 
  print('\n',coef)
  return coef

def predict(X, coef):
  output = coef[0] + np.dot(X, coef[1:])
  return output

# print(inputs[1][1])
gradientDescent(inputs, target)
# for i in range(n):
# plt.plot(inputs,target, 'bo')
# plt.plot(coef*np.arange(target.max(), step=target.max()/1000),target, 'r')
# plt.show()
