import tools
import pickle
import plot_tools
import graph_metrics
from igraph import *
import multiprocessing
from itertools import repeat
from datetime import date, timedelta

import time


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
                current_week = str(current_date.isocalendar()[1]) + "-" + \
                                              str(current_date.isocalendar()[0])
                nodes_list = tools.read_nodes_csv(path + relation_type + "/" + current_week + "/" + current_day
                                                  + "/" + "politicsNodes" + entity_type + ".csv")
                edges_list = tools.read_edges_csv(path + relation_type + "/" + current_week + "/" + current_day
                                                  + "/" + "politicsEdges" + entity_type + ".csv")

                current_graph = Graph(n=len(nodes_list), vertex_attrs={'name': nodes_list})

                for edge in edges_list:
                    current_graph.add_edge(edge[0], edge[1], weight=edge[2])

                global_metrics_dict_list['Avg_Degree'].append(mean(current_graph.degree()))
                global_metrics_dict_list['Avg_W_Degree'].append(graph_metrics.avg_weighted_degree(current_graph))
                global_metrics_dict_list['C_Coefficient'].append(current_graph.transitivity_avglocal_undirected())
                louvain = current_graph.community_multilevel()
                global_metrics_dict_list['Modularity'].append(current_graph.modularity(louvain))
                global_metrics_dict_list['Avg_Path_Length'].append(current_graph.average_path_length(directed=False))
                global_metrics_dict_list['Density'].append(current_graph.density())
                global_metrics_dict_list['Dates'].append(current_date)

                global_metrics_dict_list['Betweennes'].append(mean(current_graph.betweenness(directed=False)))
                global_metrics_dict_list['Closeness'].append(mean(current_graph.closeness()))
                global_metrics_dict_list['Eigenvector'].append(mean(current_graph.
                                                                    eigenvector_centrality(directed=False)))
                global_metrics_dict_list['Pagerank'].append(mean(current_graph.personalized_pagerank(directed=False)))

                global_metrics_dict_list['Connected_Components'].append(len(current_graph.components()))
                global_metrics_dict_list['Number_of_Edges'].append(current_graph.ecount())
                global_metrics_dict_list['Number_of_Nodes'].append(current_graph.vcount())
                global_metrics_dict_list['Number_of_Articles'].append(tools.count_articles(current_date))

            # save pickle file
            save_metrics = open("/home/iraklis/PycharmProjects/graph_analysis/pickle_files/"
                                + relation_type + "_" + entity_type + "_dict.pickle", "wb")
            pickle.dump(global_metrics_dict_list, save_metrics)
            save_metrics.close()
            plot_tools.draw_global_metrics(global_metrics_dict_list, relation_type, entity_type)
            plot_tools.draw_global_stats(global_metrics_dict_list, relation_type, entity_type)
            plot_tools.draw_global_centralities(global_metrics_dict_list, relation_type, entity_type)


# calculating the plot by adding the current day
def incremental_graph_metrics(current_date, entities_types, relations_types):
    # Article Article_Sentence Sentence
    path = "/home/iraklis/PycharmProjects/newsMiningVol2/WindowGraphs/"

    # Article Article_Sentence Sentence
    for relation_type in relations_types:
        # P L O LO PL PO PLO
        for entity_type in entities_types:
            # Load pickle file
            load_metrics = open("/home/iraklis/PycharmProjects/graph_analysis/pickle_files/"
                                + relation_type + "_" + entity_type + "_dict.pickle", "rb")
            global_metrics_dict_list = pickle.load(load_metrics)
            load_metrics.close()

            current_day = str(current_date.year) + "-" + str(current_date.month) + "-" + \
                          str(current_date.day)
            current_week = str(current_date.isocalendar()[1]) + "-" + str(current_date.isocalendar()[0])
            nodes_list = tools.read_nodes_csv(path + relation_type + "/" + current_week + "/" + current_day
                                              + "/" + "politicsNodes" + entity_type + ".csv")
            edges_list = tools.read_edges_csv(path + relation_type + "/" + current_week + "/" + current_day
                                              + "/" + "politicsEdges" + entity_type + ".csv")
            # Adding nodes to graph
            current_graph = Graph(n=len(nodes_list), vertex_attrs={'name': nodes_list})
            # Adding edges to graph
            for edge in edges_list:
                current_graph.add_edge(edge[0], edge[1], weight=edge[2])

            global_metrics_dict_list['Avg_Degree'].append(mean(current_graph.degree()))
            global_metrics_dict_list['Avg_W_Degree'].append(graph_metrics.avg_weighted_degree(current_graph))
            global_metrics_dict_list['C_Coefficient'].append(current_graph.transitivity_avglocal_undirected())
            louvain = current_graph.community_multilevel()
            global_metrics_dict_list['Modularity'].append(current_graph.modularity(louvain))
            global_metrics_dict_list['Avg_Path_Length'].append(current_graph.average_path_length(directed=False))
            global_metrics_dict_list['Density'].append(current_graph.density())
            global_metrics_dict_list['Dates'].append(current_date)

            global_metrics_dict_list['Betweennes'].append(mean(current_graph.betweenness(directed=False)))
            global_metrics_dict_list['Closeness'].append(mean(current_graph.closeness()))
            global_metrics_dict_list['Eigenvector'].append(mean(current_graph.
                                                                eigenvector_centrality(directed=False)))
            global_metrics_dict_list['Pagerank'].append(mean(current_graph.personalized_pagerank(directed=False)))

            global_metrics_dict_list['Connected_Components'].append(len(current_graph.components()))
            global_metrics_dict_list['Number_of_Edges'].append(current_graph.ecount())
            global_metrics_dict_list['Number_of_Nodes'].append(current_graph.vcount())
            global_metrics_dict_list['Number_of_Articles'].append(tools.count_articles(current_date))

            # save pickle file
            save_metrics = open("/home/iraklis/PycharmProjects/graph_analysis/pickle_files/"
                                + relation_type + "_" + entity_type + "_dict.pickle", "wb")
            pickle.dump(global_metrics_dict_list, save_metrics)
            save_metrics.close()

            print(str(entities_types) + "a")
            plot_tools.draw_global_metrics(global_metrics_dict_list, relation_type, entity_type)
            plot_tools.draw_global_stats(global_metrics_dict_list, relation_type, entity_type)
            plot_tools.draw_global_centralities(global_metrics_dict_list, relation_type, entity_type)


# Pivot function to be able to parallel call
# calculate_graph_metrics with many arguments
def function_wrapper(ent_types):
    # call the target function
    return incremental_graph_metrics(e_date, ent_types, relation_types)


if __name__ == "__main__":
    start_time = time.time()
    s_date = date(2018, 1, 13)
    e_date = date(2018, 1, 22)

    par_entity_types = [["P"], ["L"], ["O"], ["LO"], ["PL"], ["PO"], ["PLO"]]
    # ser_entity_types = ["P", "L", "O", "LO", "PL", "PO", "PLO"]
    relation_types = ["Article", "Sentence", "Article_Sentence"]

    # Serial
    # calculate_graph_metrics(s_date, e_date, ser_entity_types, relation_types)

    # Parallel
    num_of_cpus = len(par_entity_types)
    p = multiprocessing.Pool(processes=num_of_cpus)
    pool_persons_distances = p.map(function_wrapper, par_entity_types)
    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))

    # incremental_graph_metrics(e_date, par_entity_types, relation_types)
