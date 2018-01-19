import tools
import graph_metrics
from igraph import *
from datetime import date, timedelta


def calculate_graph_metrics(start_date, end_date, entities_types, relations_types):
    # Article Article_Sentence Sentence
    path = "/home/iraklis/PycharmProjects/newsMiningVol2/WindowGraphs/"
    date_range_list = list(tools.date_range(start_date, end_date + timedelta(days=1)))


    # Article Article_Sentence Sentence
    for relation_type in relations_types:
        # P L O LO PL PO PLO
        for entity_type in entities_types:
            global_metrics_dict_list = defaultdict(list)
            for current_date in date_range_list:
                # /home/iraklis/PycharmProjects/newsMiningVol2/WindowGraphs/Article/2-2018/2018-1-13/politicsEdgesL.csv

                current_day = str(current_date.year) + "-" + str(current_date.month) + "-" + \
                              str(current_date.day)
                # current_week = str(current_date.strftime("%W")) + "-" + str(current_date.strftime("%Y"))
                current_week = current_week = str(current_date.isocalendar()[1]) + "-" + \
                                              str(current_date.isocalendar()[0])
                nodes_list = tools.read_nodes_csv(path + relation_type + "/" + current_week + "/" + current_day
                                                  + "/" + "politicsNodes" + entity_type + ".csv")
                edges_list = tools.read_edges_csv(path + relation_type + "/" + current_week + "/" + current_day
                                                  + "/" + "politicsEdges" + entity_type + ".csv")

                current_graph = Graph(n=len(nodes_list), vertex_attrs={'name': nodes_list})

                for edge in edges_list:
                    current_graph.add_edge(edge[0], edge[1], weight=edge[2])

                global_metrics_dict_list['Avg_Degree'].append((mean(current_graph.degree()), current_day))
                global_metrics_dict_list['Avg_W_Degree'].append((graph_metrics.avg_weighted_degree(current_graph),
                                                                current_day))
                global_metrics_dict_list['C_Coefficient'].append((current_graph.transitivity_avglocal_undirected(),
                                                                  current_day))
                louvain = current_graph.community_multilevel()
                global_metrics_dict_list['Modularity'].append((current_graph.modularity(louvain), current_day))
                global_metrics_dict_list['Avg_Path_Length'].append((current_graph.average_path_length(directed=False),
                                                                    current_day))
                print("OK")
                w = input("Waiting")


if __name__ == "__main__":
    s_date = date(2018, 1, 13)
    e_date = date(2018, 1, 17)

    calculate_graph_metrics(s_date, e_date, ["P"], ["Sentence"])
