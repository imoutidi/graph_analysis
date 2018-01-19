from igraph import *


def avg_weighted_degree(graph):

    graph_weight_sum = 0
    for i in range(graph.vcount()):
        node_weight_sum = 0
        for edge in graph.es.select(_from=i):
            node_weight_sum += edge['weight']
        for edge in graph.es.select(_to=i):
            node_weight_sum += edge['weight']
        graph_weight_sum += node_weight_sum
    return graph_weight_sum / graph.vcount()
