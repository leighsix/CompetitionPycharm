import operator
import networkx as nx


class GraphAnalysis:

    def pagerank_ordering(self, graph):
        pagerank = nx.pagerank(graph)
        pagerank_order = sorted(pagerank.items(), key=operator.itemgetter(1), reverse=True)
        return pagerank_order    # [(node number, value), ()....]

    def cluster_ordering(self, graph):
        clustering = nx.clustering(graph)
        cluster_order = sorted(clustering.items(), key=operator.itemgetter(1), reverse=True)
        return cluster_order   # [(node number, value), ()....]

    def degree_ordering(self, graph):


    def eigen_vertor_centrality(self, graph):

    def hub_and_authority(self, graph):
        h, a = nx.hits(graph)
        hub_order = sorted(h.items(), key=operator.itemgetter(1), reverse=True)
        authority_order = sorted(a.items(), key=operator.itemgetter(1), reverse=True)
        return hub_order, authority_order   # [(node number, value), ()....]









