from igraph import *

g = Graph.GRG(30, 0.25)

print(g.degree())

print(g.degree([2, 4, 7, 8, 12]))

print(g.pagerank()[0:10])

ebs = g.edge_betweenness()
max_eb = max(ebs)
print([g.es[idx].tuple for idx, eb in enumerate(ebs) if eb == max_eb])

print(g.vs.degree())  # == g.degree()
print(g.vs[3].degree())  # == g.degree(3)

print(g.vs.select(_degree=g.maxdegree()).degree())

g1 = Graph.Full(20)
only_odd_vertices = g1.vs.select(lambda vertex: vertex.index % 2 == 1)
print([v.index for v in only_odd_vertices])  # printing the vertices of the sequence
for edge in g1.es.select(_within=[2, 3, 4]):
    print(edge.index)

# layout = g1.layout_kamada_kawai()  # or g1.layout("kamada_kawai")
layout = g1.layout("rt", 2)

l1 = g1.layout("kk")
plot(g1, layout=l1)



