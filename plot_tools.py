import matplotlib.pyplot as plt
import matplotlib


def draw_global_graphs(global_dict_list):
    dates = matplotlib.dates.date2num(global_dict_list['Dates'])
    cc = global_dict_list['C_Coefficient']

    plt.plot_date(dates, cc, 'b-', label='cc')
    plt.xlabel("Date")
    plt.ylabel("Clustering\nCoefficient")
    plt.title("CC Metric")
    plt.legend()
    plt.show()

    return 0
