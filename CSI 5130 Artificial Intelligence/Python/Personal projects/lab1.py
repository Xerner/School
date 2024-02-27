import time
import numpy as np
import matplotlib.pyplot as plt

print('Required Libraries:\ttime, numpy, matplotlib')

n_iterations = 1000
n = 100
learningRate = 0.01

np.random.seed(42)
X = 3*np.random.rand(n,1)
y = 9 + 2*X+np.random.rand(n,1)

def addRandomness():
  # add some outliers to the data
  sign = 1
  for i in range(int(n/10)):
    i*=10
    # print(y[i][0])
    y[i][0]+=25*np.random.rand()*sign
    sign*=-1

# w0 + w1.X
def predict(X, coef):
  output = coef[0] + np.dot(X, coef[1])
  return output

# SGD with L1 loss optimization
def L1fit(X, y):
  time_ = time.time()
  coef = np.zeros(2)
  for i in range(n_iterations):
    for xi, expected_value in zip(X, y):
      predicted_value = predict(xi, coef)
      # y2[xi] = predicted_value
      coef[0] -= learningRate * ((predicted_value - expected_value) / abs(predicted_value - expected_value)) * 1
      coef[1] -= learningRate * ((predicted_value - expected_value) / abs(predicted_value - expected_value)) * xi
  print('Runtime:\t', round(time.time() - time_,2),'sec')
  print('L1 Coeff:\t', coef)
  return coef

# SGD with L2 loss optimization
def L2fit(X, y):
  time_ = time.time()
  coef = np.zeros(2)
  for i in range(n_iterations):
    for xi, expected_value in zip(X, y):
      predicted_value = predict(xi, coef)
      # y2[xi] = predicted_value
      coef[0] -= learningRate * (predicted_value - expected_value) * 1
      coef[1] -= learningRate * (predicted_value - expected_value) * xi
  print('Runtime:\t', round(time.time() - time_,2),'sec')
  print('L2 Coeff:\t', coef)
  return coef

print('Model:\t\t\ty=mx+b')
print('Iterations:\t\t', n_iterations)
print('datapoints:\t\t',n)
print('Learning Rate:\t\t', learningRate)
print('Expected runtime:\t 1~ sec')
print('----------------------------------------------------------')
print('Without outliers')
L1coef = L1fit(X, y)
L1 = L1coef[1]*X+ L1coef[0]
print('----------------------------------------------------------')
L2coef = L2fit(X, y)
L2 = L2coef[1]*X+ L2coef[0]

print('Close the graph to continue to the example with randomess')
plt.plot(X, y, 'co')
plt.plot(X, L1, 'r', label='L1')
plt.plot(X, L2, 'b', label='L2')
plt.title("L1 vs L2 Loss no outliers")
plt.xlabel("Sample 1 Data")
plt.ylabel("Sample 2 Data")
plt.legend()
plt.show()

print('----------------------------------------------------------')
print('With outliers')
addRandomness()
L1coefOutliers = L1fit(X, y)
L1 = L1coef[1]*X+ L1coef[0]
print('----------------------------------------------------------')
L2coefOutliers = L2fit(X, y)
L2 = L2coef[1]*X+ L2coef[0]
print('----------------------------------------------------------')
print('Statistics')
print('L1 Coefficients')
print('No outliers:\t', L1coef)
print('Outliers:\t', L1coefOutliers)
print('Difference:\t', L1coef-L1coefOutliers)
print('L2 Coefficients')
print('No outliers:\t', L2coef)
print('Outliers:\t', L2coefOutliers)
print('Difference:\t', L2coef-L2coefOutliers)
print("""L2 loss diverges from the data, while L1 loss stays close. 
This is because the squared difference in L2 loss causes outliers to heavily affect the models coefficients.
In contrast, L2 loss should be slightly faster computation time compared to L1, since it contains less arithmetic.""")

plt.plot(X, y, 'co')
plt.plot(X, L1, 'r', label='L1')
plt.plot(X, L2, 'b', label='L2')
plt.title("L1 vs L2 Loss with outliers")
plt.xlabel("Sample 1 Data")
plt.ylabel("Sample 2 Data")
plt.legend()
plt.show()