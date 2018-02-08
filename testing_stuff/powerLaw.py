import powerlaw
import datetime
from tools import form_graph
import graph_metrics
from scipy import stats
import matplotlib.pyplot as plt
from math import log10
import matplotlib


def power_law_test(data):
    fit = powerlaw.Fit(data, discrete=True)
    print("Power law test results:")
    print("xmin", fit.xmin)
    print("alpha", fit.alpha)
    print("D", fit.D)


def normal_distribution_test(data):
    print(stats.normaltest(data))


def create_plot_data(data):
    sorted_d_list = sorted(data)
    print(sorted_d_list)

    values = list()
    frequencies = list()
    values.append(sorted_d_list[0])

    count = 0
    idx = 0
    for el in sorted_d_list:
        if values[idx] < el:
            values.append(el)
            idx += 1
            frequencies.append(count)
            count = 0
        count += 1
    frequencies.append(count)
    return values, frequencies


def draw(v, f):
    plt.scatter(v, f, label='Value', color='green')
    # plt.errorbar(v, f, yerr=10)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Distribution")
    plt.show()


current_date = datetime.date.today() - datetime.timedelta(1)
current_graph = form_graph(current_date, "Sentence", "P")

degree_list = current_graph.degree()
parameters = eval("stats.powerlaw.fit(degree_list)")
print(stats.kstest(degree_list, "powerlaw", args=parameters))
val, freq = create_plot_data(degree_list)

# log_val = [log10(i) for i in val[1:]]
# log_freq = [log10(i) for i in freq[1:]]

draw(val, freq)



weighed_degree_list = graph_metrics.weighted_degree(current_graph)
val, freq = create_plot_data(weighed_degree_list)


draw(val, freq)

betweenness_list = current_graph.betweenness(directed=False)
val, freq = create_plot_data(betweenness_list)

draw(val, freq)

closeness_list = current_graph.closeness()
val, freq = create_plot_data(closeness_list)

draw(val, freq)

eigenvector_list = current_graph.eigenvector_centrality(directed=False)
val, freq = create_plot_data(eigenvector_list)
draw(val, freq)

pagerank_list = current_graph.personalized_pagerank(directed=False)
val, freq = create_plot_data(pagerank_list)
draw(val, freq)





