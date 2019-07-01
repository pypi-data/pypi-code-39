from statistics import mean
import numpy as np

class LSR:

    def __init__(self):
        self.slope = 0 #This represents the slope of our regression
        self.intercept = 0 #This represents the intercept of our regression
        self.r_squared = 0 #This represents the r^2 squared of our regression

    def Model(self, x, y):
        temp_x = np.array(x, dtype=np.float64) #numpy array of our x values
        temp_y = np.array(y, dtype=np.float64) #numpy array of our y values
        if(temp_x.shape == temp_y.shape):
            self.slope = ( ((mean(temp_x) * mean(temp_y)) - mean(temp_x * temp_y))/((mean(temp_x)*mean(temp_x)) - mean(temp_x*temp_x)) )
            self.intercept = mean(temp_y) - (self.slope * mean(temp_x))
            temp_y_approx = self.slope*temp_x + self.intercept
            self.r_squared = 1 - ( (np.sum((temp_y - temp_y_approx)**2))/(np.sum((temp_y - mean(temp_y))**2)) )
            print("Slope: ", self.slope)
            print("Offset: ", self.intercept)
            print("R^2 Squared: ", self.r_squared)
            del temp_x, temp_y, temp_y_approx
        else:
            print("X and Y are not the same shape")
