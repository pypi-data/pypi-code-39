from statistics import mean
import numpy as np

class LSR:

    def __init__(self):
        self.slope = 0 #This represents the slope of our regression
        self.intercept = 0 #This represents the intercept of our regression

    def Model(self, x, y):
        temp_x = np.array(x, dtype=np.float64) #numpy array of our x values
        temp_y = np.array(y, dtype=np.float64) #numpy array of our y values
        if(temp_x.shape == temp_y.shape):
            self.slope = ( ((mean(temp_x) * mean(temp_y)) - mean(temp_x * temp_y))/((mean(temp_x)*mean(temp_x)) - mean(temp_x*temp_x)) )
            self.intercept = mean(temp_y) - (self.slope * mean(temp_x))
            print("Slope: ", self.slope)
            print("Offset: ", self.intercept)
            del temp_x, temp_y
        else:
            print("X and Y are not the same shape")
