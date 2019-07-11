import math
import matplotlib.pyplot as plt

from .general_distribution import Distribution


class Binomial(Distribution):
    """
    Binomial distribution class for calculating and visualizing a
    Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data (list of floats) a list of floats extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
    """

    def __init__(self, prob=.5, size=20):
        self.p = prob
        self.n = size
        super().__init__(self.calculate_mean(), self.calculate_stdev())

    def __add__(self, other):
        """
        Function to add together two Binomial distributions with equal p
        Note that p is assumed the be the same for both distributions

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution
        """
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError:
            raise

        new_binomial = Binomial(self.p, self.n + other.n)
        new_binomial.mean = new_binomial.calculate_mean()
        new_binomial.stdev = new_binomial.calculate_stdev()

        return new_binomial

    def __repr__(self):
        """
        Function to output the characteristics of the Binomial instance

        Returns:
            string: characteristics of the Gaussian

        """
        return "mean {m}, standard deviation {s}, p {p}, n {n}".format(
            m=self.mean, s=self.stdev, p=self.p, n=self.n)

    def calculate_mean(self):
        """
        Function to calculate the mean from p and n

        Returns:
            float: mean of the data set
        """
        self.mean = self.n * self.p

        return self.mean

    def calculate_stdev(self):
        """
        Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set
        """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))

        return self.stdev

    def replace_stats_with_data(self):
        """
        Function to calculate p and n from the data set

        Returns:
            float: the p value
            float: the n value
        """
        self.n = len(self.data)
        self.p = 1.0 * (sum(self.data) / len(self.data))

        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n

    def pdf(self, k):
        """
        Probability density function calculator for the gaussian distribution.

        Args:
            k (float): point for calculating the probability density function

        Returns:
            float: probability density function output
        """

        return self.n_choose_k(self.n, k) * (self.p ** k) * (1 - self.p) ** (
            self.n - k)

    def plot_bar_pdf(self):
        """
        Function to plot the pdf of Binomial distribution

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """

        x = []
        y = []

        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()
