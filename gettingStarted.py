from igraph import *

g = Graph()

g.add_vertices(4)
g.add_edges([(0, 1), (1, 2), (2, 3), (3, 2)])
g.add_vertices(3)
g.add_edges([(0, 2), (1, 3), (0, 5), (4, 6), (5, 4)])
print(g)

summary(g)
g2 = Graph.Tree(256, 3)
edge_list = g2.get_edgelist()[0:20]
print(edge_list)

g3 = Graph.GRG(100, 0.3)
summary(g3)

print(g.es[0].target)
print(g.es[1].source)
print(g.es[4].index)
print(g.es[0].tuple)




