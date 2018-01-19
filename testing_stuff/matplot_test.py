import matplotlib.pyplot as plt


def example1():
    x = [1, 2, 3, 4]
    y = [4, 7, 8, 6]

    x2 = [1, 2, 3, 4]
    y2 = [10, 12, 14, 15]


    plt.plot(x, y, label='First one', color='green')
    plt.plot(x2, y2, label='Second one', color='red')
    plt.xlabel("Plot Number")
    plt.ylabel("Variable")
    plt.title("Graph1")
    plt.legend()

    plt.show()


def bar_hist():
    x = [1, 2, 3, 4, 5, 10]
    y = [4, 7, 8, 6, 3, 7]

    x2 = [2, 4, 6, 8, 10, 12]
    y2 = [1, 2, 3, 4, 5, 6]

    population_ages = [22, 10, 15, 50, 65, 99, 100, 44, 50, 33, 43, 10, 101, 30, 40, 13, 22, 23, 34, 39, 80, 77, 78, 69,
                       33, 36, 11, 13, 16, 2, 4, 10, 64, 40, 105, 129, 100, 80, 20, 88, 82, 33, 42, 68, 50, 54, 61, 52]
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]

    # plt.bar(x, y, label='Bars1')
    # plt.bar(x2, y2, label='Bars2')

    plt.hist(population_ages, bins, histtype='bar', rwidth=0.8, label='Ages')
    plt.xlabel("Plot Number")
    plt.ylabel("Variable")
    plt.title("Graph1")
    plt.legend()

    plt.show()


def scatter_plot():
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 5, 7, 7, 4, 8, 1, 2, 4, 9]

    plt.scatter(x, y, label='Skittles', color='k', marker='^', s=60)

    plt.xlabel("Plot Number")
    plt.ylabel("Variable")
    plt.title("Graph1")
    plt.legend()

    plt.show()

def stack_plot():

    days = [1, 2, 3, 4, 5]
    sleeping = [7, 8, 6, 7, 11]
    working =  [8, 9, 7, 8, 8]
    eating =   [2, 1, 3, 2, 1]
    playing =  [2, 3, 4, 2, 3]

    plt.plot([], [], color='k', label='Sleeping', linewidth=5)
    plt.plot([], [], color='c', label='Eating', linewidth=5)
    plt.plot([], [], color='r', label='Playing', linewidth=5)
    plt.plot([], [], color='b', label='Working', linewidth=5)


    plt.stackplot(days, sleeping, eating, playing, working, colors=['k', 'c', 'r', 'b'])

    plt.xlabel("Plot Number")
    plt.ylabel("Variable")
    plt.title("Graph1")
    plt.legend()
    plt.show()

stack_plot()

