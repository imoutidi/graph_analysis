import csv
from datetime import date, timedelta
from igraph import *
import pymongo


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

