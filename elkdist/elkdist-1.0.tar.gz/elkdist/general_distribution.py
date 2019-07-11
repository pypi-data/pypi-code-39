import matplotlib.pyplot as plt
import math


class Distribution:

    def __init__(self, mu=0, sigma=1):
        """
        Generic distribution class for calculating and
        visualizing a probability distribution.

        Attributes:
            mean (float) representing the mean value of the distribution
            stdev (float) representing the standard dev of the distribution
            data (list of floats) a list of floats extracted from data file
        """
        self.mean = mu
        self.stdev = sigma
        self.data = []

    def __add__(self, other):
        """
        Function to add together two distributions

        Args:
            other (Distribution): Distribution instance

        Returns:
            Distribution: Distribution instance
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Function to output the characteristics of the distribution instance

        Returns:
            string: characteristics of the distribution
        """
        raise NotImplementedError

    @staticmethod
    def n_choose_k(n, k):
        """
        Returns count of combinations

        Args:
            n (int): total number of trials
            k (int): chosen number of trials

        Returns:
        """
        f = math.factorial
        return f(n) / f(k) / f(n - k)

    def pdf(self, k):
        """
        Probability density function calculator for a distribution.

        Args:
            k (float): point for calculating the probability density function

        Returns:
            float: probability density function output
        """
        raise NotImplementedError

    def plot_histogram(self):
        """
        Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Returns:
            None
        """
        plt.figure()
        plt.hist(self.data)
        plt.xlabel('Data')
        plt.ylabel('Count')
        plt.title('Histogram of Data')
        plt.show()

    def read_data_file(self, file_name):
        """
        Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are
        stored in the data attribute.

        Args:
            file_name (string): name of a file to read from

        Returns:
            None
        """

        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()

        self.data = data_list
