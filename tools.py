import csv
import plot_tools
import pickle
from datetime import date, timedelta
from igraph import *
import pymongo
import graph_metrics
import multiprocessing


def form_graph(c_date, r_type, e_type):
    path = "/home/iraklis/PycharmProjects/newsMiningVol2/WindowGraphs/"

    current_day = str(c_date.year) + "-" + str(c_date.month) + "-" + str(c_date.day)
    current_week = str(c_date.isocalendar()[1]) + "-" + str(c_date.isocalendar()[0])
    nodes_list = read_nodes_csv(path + r_type + "/" + current_week + "/" + current_day
                                + "/" + "politicsNodes" + e_type + ".csv")
    edges_list = read_edges_csv(path + r_type + "/" + current_week + "/" + current_day
                                + "/" + "politicsEdges" + e_type + ".csv")
    # Adding nodes to graph
    c_graph = Graph(n=len(nodes_list), vertex_attrs={'name': nodes_list})
    # Adding edges to graph
    for edge in edges_list:
        c_graph.add_edge(edge[0], edge[1], weight=edge[2])

    return c_graph


def read_edges_csv(filename):
    edge_list = list()
    csv_reader = csv.reader(open(filename), delimiter=',', quotechar='"')

    next(csv_reader)
    for row in csv_reader:
        edge_list.append((int(row[0]), int(row[1]), int(row[2])))

    return edge_list


def read_nodes_csv(filename):
    node_list = list()
    csv_reader = csv.reader(open(filename), delimiter=',', quotechar='"')

    next(csv_reader)
    for row in csv_reader:
        # node_list.append(((int(row[0])), row[1]))
        node_list.append(row[1])
    return node_list


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# Given a list of nodes of a graph we create a new subgraph
def get_subgraph(node_id_list, graph):
    node_id_list.sort()
    node_name_list = list()
    for node_id in node_id_list:
        node_name_list.append(graph.vs[node_id]['name'])

    giant_comp_graph = Graph(n=len(node_name_list), vertex_attrs={'name': node_name_list})
    for edge in graph.es():
        if edge.source in node_id_list and edge.target in node_id_list:
            giant_comp_graph.add_edge(node_id_list.index(edge.source),
                                      node_id_list.index(edge.target), weight=edge['weight'])

    return giant_comp_graph


def count_articles(last_date):
    date_range_list = list(date_range(last_date - timedelta(days=6), last_date + timedelta(days=1)))
    art_num = 0
    for c_date in date_range_list:
        day = str(c_date.year) + "-" + str(c_date.month) + "-" + str(c_date.day)
        current_week = str(c_date.isocalendar()[1]) + "-" + str(c_date.isocalendar()[0])

        # Database stuff
        # Getting data from the mongo database
        client = pymongo.MongoClient()
        # Database name is minedNews
        db = client.minedArticles
        art_num += db[current_week].count({"date": day})

    return art_num


def calculate_metrics_lists(end_date, relation_type, entity_type):
    # The date of the creation of the first graph
    s_date = date(2018, 1, 13)

    date_range_list = list(date_range(s_date, end_date + timedelta(days=1)))
    # each element of the outer list corresponds to a date
    date_dir = "/home/iraklis/PycharmProjects/graph_analysis/node_metrics/"
    metrics_lists_dict = dict()
    for current_date in date_range_list:
        current_graph = form_graph(current_date, relation_type, entity_type)

        metrics_lists_dict['degree_list'] = current_graph.degree()
        metrics_lists_dict['weighted_degree_list'] = graph_metrics.weighted_degree(current_graph)
        metrics_lists_dict['betweenness_list'] = current_graph.betweenness(directed=False)
        metrics_lists_dict['closeness_list'] = current_graph.closeness()
        metrics_lists_dict['eigenvector_list'] = current_graph.eigenvector_centrality(directed=False)
        metrics_lists_dict['pagerank_list'] = current_graph.personalized_pagerank(directed=False)
        metrics_lists_dict['Names'] = current_graph.vs['name']

        year_path = date_dir + relation_type + "/" + str(current_date.year)
        if not os.path.exists(year_path):
            os.makedirs(year_path)
        month_path = year_path + "/" + str(current_date.month)
        if not os.path.exists(month_path):
            os.makedirs(month_path)
        week_path = month_path + "/" + str(current_date.isocalendar()[1])
        if not os.path.exists(week_path):
            os.makedirs(week_path)
        day_path = week_path + "/" + str(current_date.day)
        if not os.path.exists(day_path):
            os.makedirs(day_path)

        save_metrics = open("/home/iraklis/PycharmProjects/graph_analysis/node_metrics/"
                            + relation_type + "/" + str(current_date.year) + "/"
                            + str(current_date.month) + "/" + str(current_date.isocalendar()[1]) + "/"
                            + str(current_date.day) + "/" + entity_type + "_dict.pickle", "wb")
        pickle.dump(metrics_lists_dict, save_metrics)
        save_metrics.close()
    print("end off " + relation_type + " " + entity_type)


# Here we will calculate the common nodes similarities for the graph
def affinity_matrix(end_date):
    # The first window graph we got
    s_date = date(2018, 1, 13)
    # entities_types = ["P", "L", "O", "LO", "PL", "PO", "PLO"]
    # relations_types = ["Article", "Sentence", "Article_Sentence"]
    entities_types = ["P"]
    relations_types = ["Sentence"]
    date_range_list = list(date_range(s_date, end_date + timedelta(days=1)))

    # Article Article_Sentence Sentence
    for relation_type in relations_types:
        # P L O LO PL PO PLO
        for entity_type in entities_types:
            name_list = list()
            val_lol = list()

            for current_date in date_range_list:
                current_graph = form_graph(current_date, relation_type, entity_type)
                print(relation_type + " " + entity_type + " " + str(current_date) + "\n")
                # The current_graph.degree() functions returns a list with the degrees nodes
                # that correspond to the same index
                degree_list = current_graph.degree()
                # The sorted list contains the indexes of the nodes sorted regarding the max degree
                sorted_degree = sorted(range(len(degree_list)), key=lambda k: degree_list[k], reverse=True)


                print(current_graph.vs['name'][sorted_degree[0]] + " " + str(degree_list[sorted_degree[0]]))
                plot_tools.draw_entities_plot()

                w_degree_list = graph_metrics.weighted_degree(current_graph)
                sorted_w_degree = sorted(range(len(w_degree_list)), key=lambda k: w_degree_list[k], reverse=True)

                bet_list = current_graph.betweenness(directed=False)
                sorted_bet_list = sorted(range(len(bet_list)), key=lambda k: bet_list[k], reverse=True)


def node_metrics_parallel(fns, in_date):
    proc = []
    # The computations on the PLO graphs are taking most of the time so we
    # assign one core for each PLO graph (second for loop)
    ent_types = ["P", "L", "O", "LO", "PL", "PO", "PLO"]
    rel_types = ["Article", "Sentence", "Article_Sentence"]
    for ent_type in ent_types:
        for rel_type in rel_types:
            p = multiprocessing.Process(target=fns, args=(in_date, rel_type, ent_type,))
            p.start()
            proc.append(p)
    for pr in proc:
        pr.join()


if __name__ == "__main__":
    n_date = date(2018, 2, 2)
    # calculate_metrics_lists(n_date)
    node_metrics_parallel(calculate_metrics_lists, n_date)
