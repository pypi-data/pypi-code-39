import matplotlib.pyplot as plt


def plot_conv(conv):
    plt.xlabel('Number of function evaluations')
    plt.ylabel('Objective function')
    plt.title('Convergence graph')
    plt.grid(True)
    plt.plot(conv, 'b', label='line')
    plt.show()


