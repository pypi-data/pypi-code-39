# import the mse module
from pymse import mse

# create an example dataset
import numpy as np
dataset = np.sin(np.linspace(0, 2 * np.pi, 1000))

# calculate the MSE, by default scale=1-20, m=2 and r=0.15
# result = mse(dataset)
# print(result)


# custom scale
scale = [1, 2, 3, 4, 5, 6]
result = mse(dataset, scale)
print(result)


# custom m
scale = [1, 2, 3, 4, 5, 6]
M = [2, 3, 4]
result = mse(dataset, scale, m=M)
print(result)

# custom r
scale = [1, 2, 3, 4, 5, 6]
R = np.linspace(0.15, 0.25, 4)
result = mse(dataset, scale, r=R)
print(result)


# custom m and r
scale = range(1, 10)
M = range(2, 6)
R = np.linspace(0.15, 0.25, 3)
result = mse(dataset, scale, m=M, r=R)
print(result)
