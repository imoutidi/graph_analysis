import csv
import plot_tools
from datetime import date, timedelta
from igraph import *
import pymongo
import graph_metrics


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


# Here we will calculate the common nodes similarities for the graph
def common_nodes(end_date):
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



if __name__ == "__main__":
    n_date = date(2018, 1, 25)
