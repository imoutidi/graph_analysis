import matplotlib.pyplot as plt
from testing_stuff import matplot_test
import csv
import numpy as np
import urllib
import matplotlib.dates as mdates

def read_csv_file():
    x = []
    y = []
    with open('example.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(int(row[0]))
            y.append(int(row[1]))

    plt.plot(x, y, label="loaded from file")

    plt.xlabel("Plot Number")
    plt.ylabel("Variable")
    plt.title("Graph1")
    plt.legend()

    plt.show()


def read_csv_numpy():
    x, y = np.loadtxt('example.csv', delimiter=',', unpack=True)

    plt.plot(x, y, label="Loaded from file\nwith numpy")

    plt.xlabel("Plot Number")
    plt.ylabel("Variable")
    plt.title("Graph1")
    plt.legend()

    plt.show()



def sub_plots():
    y1 = [1, 2, 3, 4, 5, 6]
    y2 = [33, 29, 28, 31, 29, 32]
    y3 = [42, 41, 44, 49, 46, 40]
    y4 = [59, 58, 60, 54, 62, 64]
    y5 = [11, 12, 13, 11, 10, 14]
    y6 = [22, 33, 44, 55, 66, 77]
    x = np.arange(len(y1))  # 1, 2, 3, 4, 5, 6, ... len

    fig1 = plt.figure(1)
    fig1.suptitle("Figure 1")

    sub_plot1 = fig1.add_subplot(2, 2, 1)
    sub_plot1.plot(x, y1, 'blue')

    sub_plot2 = fig1.add_subplot(2, 2, 2)
    sub_plot2.plot(x, y2, 'r')

    sub_plot3 = fig1.add_subplot(2, 2, 3)
    sub_plot3.plot(x, y3, 'c')

    sub_plot4 = fig1.add_subplot(2, 2, 4)
    sub_plot4.plot(x, y4, 'k')

    plt.show()

sub_plots()



