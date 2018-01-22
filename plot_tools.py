import matplotlib.pyplot as plt
import matplotlib


# Drawing plot of Clustering Coefficient, Degree, Weighted Degree,
# Modularity and AVG Path Length
def draw_global_metrics(global_dict_list):
    dates = matplotlib.dates.date2num(global_dict_list['Dates'])
    cc = global_dict_list['C_Coefficient']
    avg_d = global_dict_list['Avg_Degree']
    avg_w_d = global_dict_list['Avg_W_Degree']
    mod = global_dict_list['Modularity']
    avg_p_len = global_dict_list['Avg_Path_Length']
    den = global_dict_list['Density']

    all_metrics = [cc, avg_d, avg_w_d, avg_p_len, mod, den]
    metrics_labels = ['Clustering Coefficient', 'Average Degree', 'Average Weighted Degree', 'Average Path Length',
                      'Modularity', 'Density']

    figure, ax_plots = plt.subplots(2, 3)
    figure.set_size_inches(11, 7)

    for index, ax in enumerate(figure.axes):
        ax.plot_date(dates, all_metrics[index], 'b-', marker='o')
        ax.set_ylabel(metrics_labels[index])
        ax.set_xlabel('Date')
        matplotlib.pyplot.sca(ax)
        plt.xticks(rotation=45)

    figure.suptitle('Graph Metrics')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    figure.savefig('Metrics.png', bbox_inches='tight')
    plt.show()


def draw_global_stats(global_dict_list):
    dates = matplotlib.dates.date2num(global_dict_list['Dates'])
    con_comp = global_dict_list['Connected_Components']
    node_num = global_dict_list['Number_of_Nodes']
    edge_num = global_dict_list['Number_of_Edges']
    art_num = global_dict_list['Number_of_Articles']

    all_metrics = [con_comp, node_num, edge_num, art_num]
    metrics_labels = ['Connected_Components', 'Number_of_Nodes', 'Number_of_Edges', 'Number_of_Articles']

    figure, ax_plots = plt.subplots(2, 2)
    figure.set_size_inches(11, 7)

    for index, ax in enumerate(figure.axes):
        ax.plot_date(dates, all_metrics[index], 'b-', marker='o')
        ax.set_ylabel(metrics_labels[index])
        ax.set_xlabel('Date')
        matplotlib.pyplot.sca(ax)
        plt.xticks(rotation=45)

    figure.suptitle('Graph Statistics')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    figure.savefig('Statistics.png', bbox_inches='tight')
    plt.show()


def draw_global_centralities(global_dict_list):
    dates = matplotlib.dates.date2num(global_dict_list['Dates'])
    close = global_dict_list['Closeness']
    bet = global_dict_list['Betweennes']
    eigen = global_dict_list['Eigenvector']
    page = global_dict_list['Pagerank']

    all_metrics = [close, bet, eigen, page]
    metrics_labels = ['Closeness', 'Betweennes', 'Eigenvector', 'Pagerank']

    figure, ax_plots = plt.subplots(2, 2)
    figure.set_size_inches(11, 7)

    for index, ax in enumerate(figure.axes):
        ax.plot_date(dates, all_metrics[index], 'b-', marker='o')
        ax.set_ylabel(metrics_labels[index])
        ax.set_xlabel('Date')
        matplotlib.pyplot.sca(ax)
        plt.xticks(rotation=45)

    figure.suptitle('Graph Centralities')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    figure.savefig('Centralities.png', bbox_inches='tight')
    plt.show()









