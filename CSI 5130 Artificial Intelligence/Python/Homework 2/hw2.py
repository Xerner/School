import time
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def kmeans(x, k, n_iterations):
  # Randomly choose points to be our centroids
  idx = np.random.choice(len(x), k, replace=False)
  
  centroids = x[idx, :]

  # finding the distance between centroids and all the data points
  distances = cdist(x, centroids,'euclidean')
  
  # Centroid with the minimum Distance
  points = np.array([np.argmin(distance) for distance in distances]) # for each point, 

  # Learnin time
  time_ = time.time()
  for _ in range(n_iterations): 
    print('Epoch',_,'\t', round(time.time() - time_,2),'sec')

    # We re-calculate our centroids every iteration
    centroids = []
    for j in range(k):
      # Re-calculate our centroids by taking the mean of the cluster it belongs to
      temp_centroid = x[points==j].mean(axis=0)
      centroids.append(temp_centroid)

    # Update our centroids
    centroids = np.vstack(centroids)
    
    distances = cdist(x, centroids ,'euclidean')
    points = np.array([np.argmin(i) for i in distances])
  
  return points, centroids

# Load image data
img = mpimg.imread('./lake.jpg')
x_resolution = img.shape[0]
y_resolution = img.shape[1]
img = img[:,:,0:3] # cut off alpha values

k_clusters = 20
iterations = 10

################################################################### 1D
print('Running K-means over 1D data\n')
# Reshape array for processing 3D
data_1D = img[:,:,0]
data_1D = data_1D.reshape((x_resolution*y_resolution, 1))
print('Data points\t',data_1D.shape[0],'\n','Clusters (K)\t',k_clusters,'\n','Iterations\t',iterations)
time_ = time.time()
labels_1D, centroids_1D = kmeans(data_1D,k_clusters,iterations)
labels_1D = labels_1D.reshape((x_resolution, y_resolution, 1))
print('Runtime:\t', round(time.time() - time_,2),'sec')
print('Centroids\n',centroids_1D)
################################################################### 3D
print('Running K-means over 3D data\n')
# Reshape array for processing 3D
data_3D = img
data_3D = data_3D.reshape((x_resolution*y_resolution, 3))
print('Data points\t',data_3D.shape[0],'\n','Clusters (K)\t',k_clusters,'\n','Iterations\t',iterations)
time_ = time.time()
labels_3D, centroids_3D = kmeans(data_3D,k_clusters,iterations)
labels_3D = labels_3D.reshape((x_resolution, y_resolution, 1))
print('Runtime:\t', round(time.time() - time_,2),'sec')
print('Centroids\n',centroids_3D)
################################################################### 5D
print('Running K-means over 5D data\n')
# Reshape array for processing 5D
data_5D = img[:,:,0:3]
new_data_5D = np.zeros((x_resolution, y_resolution, 5))
for x in range(x_resolution):
  for y in range(y_resolution):
    for k in range(5):
      if k < 3:
        new_data_5D[x, y, k] = data_5D[x, y, k]
      elif k == 3:
        new_data_5D[x, y, k] = x
      else:
        new_data_5D[x, y, k] = y

new_data_5D = new_data_5D.reshape((x_resolution*y_resolution, 5))
print('Data points\t',new_data_5D.shape[0],'\n','Clusters (K)\t',k_clusters,'\n','Iterations\t',iterations)
time_ = time.time()
labels_5D, centroids_5D = kmeans(new_data_5D,k_clusters,iterations)
labels_5D = labels_5D.reshape((x_resolution, y_resolution, 1))
print('Runtime:\t', round(time.time() - time_,2),'sec')
print('Centroids\n',centroids_5D)

# Visualize the results

# Initialise the subplot function using number of rows and columns 
figure, axis = plt.subplots(2, 3) 

# # Original Image
img = img.reshape((x_resolution, y_resolution, 3))
axis[0,1].imshow(img)
axis[0,1].set_title("Original Image") 
  
# 1D
axis[1,0].imshow(labels_1D, cmap='cividis')
axis[1,0].set_title("Clustering with 1 Color")

# 3D 
axis[1,1].imshow(labels_3D, cmap='cividis')
axis[1,1].set_title("Clustering with RGB")
  
# 5D 
axis[1,2].imshow(labels_5D, cmap='cividis')
axis[1,2].set_title("Clustering with RGB and (X,Y)")

plt.show()
