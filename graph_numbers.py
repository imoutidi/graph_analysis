import tools
import pickle
import plot_tools
import graph_metrics
from igraph import *
import multiprocessing
from datetime import date, timedelta

import time


def calculate_graph_metrics(start_date, end_date, entities_types, relations_types):
    # Article Article_Sentence Sentence
    date_range_list = list(tools.date_range(start_date, end_date + timedelta(days=1)))

    # Article Article_Sentence Sentence
    for relation_type in relations_types:
        # P L O LO PL PO PLO
        for entity_type in entities_types:
            global_metrics_dict_list = defaultdict(list)
            for current_date in date_range_list:
                current_graph = tools.form_graph(current_date, relation_type, entity_type)

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
    for relation_type in relations_types:
        # P L O LO PL PO PLO
        for entity_type in entities_types:
            # Load pickle file
            load_metrics = open("/home/iraklis/PycharmProjects/graph_analysis/pickle_files/"
                                + relation_type + "_" + entity_type + "_dict.pickle", "rb")
            global_metrics_dict_list = pickle.load(load_metrics)
            load_metrics.close()

            current_graph = tools.form_graph(current_date, relation_type, entity_type)
            # Metrics to use for affinity matrix
            degree_list = current_graph.degree()
            weighted_degree_list = graph_metrics.weighted_degree(current_graph)
            betweenness_list = current_graph.betweenness(directed=False)
            closeness_list = current_graph.closeness()
            eigenvector_list = current_graph.eigenvector_centrality(directed=False)
            pagerank_list = current_graph.personalized_pagerank(directed=False)

            global_metrics_dict_list['Avg_Degree'].append(mean(degree_list))
            global_metrics_dict_list['Avg_W_Degree'].append(mean(weighted_degree_list))
            global_metrics_dict_list['C_Coefficient'].append(current_graph.transitivity_avglocal_undirected())
            louvain = current_graph.community_multilevel()
            global_metrics_dict_list['Modularity'].append(current_graph.modularity(louvain))
            global_metrics_dict_list['Avg_Path_Length'].append(current_graph.average_path_length(directed=False))
            global_metrics_dict_list['Density'].append(current_graph.density())
            global_metrics_dict_list['Dates'].append(current_date)

            global_metrics_dict_list['Betweennes'].append(mean(betweenness_list))
            global_metrics_dict_list['Closeness'].append(mean(closeness_list))
            global_metrics_dict_list['Eigenvector'].append(mean(eigenvector_list))
            global_metrics_dict_list['Pagerank'].append(mean(pagerank_list))


            global_metrics_dict_list['Connected_Components'].append(len(current_graph.components()))
            global_metrics_dict_list['Number_of_Edges'].append(current_graph.ecount())
            global_metrics_dict_list['Number_of_Nodes'].append(current_graph.vcount())
            global_metrics_dict_list['Number_of_Articles'].append(tools.count_articles(current_date))

            # save pickle file
            save_metrics = open("/home/iraklis/PycharmProjects/graph_analysis/pickle_files/"
                                + relation_type + "_" + entity_type + "_dict.pickle", "wb")
            pickle.dump(global_metrics_dict_list, save_metrics)
            save_metrics.close()

            print(str(entities_types) + " " + str(relations_types))
            plot_tools.draw_global_metrics(global_metrics_dict_list, relation_type, entity_type)
            plot_tools.draw_global_stats(global_metrics_dict_list, relation_type, entity_type)
            plot_tools.draw_global_centralities(global_metrics_dict_list, relation_type, entity_type)


def run_in_parallel(fns, in_date):
    proc = []
    # The computations on the PLO graphs are taking most of the time so we
    # assign one core for each PLO graph (second for loop)
    list_rels = [["Article"], ["Sentence"], ["Article_Sentence"]]
    ent_types = [["P", "L", "O"], ["LO"], ["PL"], ["PO"]]
    rel_types = ["Article", "Sentence", "Article_Sentence"]
    for ent_type in ent_types:
        p = multiprocessing.Process(target=fns, args=(in_date, ent_type, rel_types,))
        p.start()
        proc.append(p)
    for rel_type in list_rels:
        p2 = multiprocessing.Process(target=fns, args=(in_date, ["PLO"], rel_type,))
        p2.start()
        proc.append(p2)
    for pr in proc:
        pr.join()


if __name__ == "__main__":
    start_time = time.time()
    s_date = date(2018, 1, 13)
    e_date = date.today() - timedelta(1)
    # ser_entity_types = ["P", "L", "O", "LO", "PL", "PO", "PLO"]

    # Serial
    # calculate_graph_metrics(s_date, e_date, ser_entity_types, relation_types)

    # Parallel and incremental
    run_in_parallel(incremental_graph_metrics, e_date)
    print("--- %s seconds ---" % (time.time() - start_time))
    # --- 108.33 seconds ---
