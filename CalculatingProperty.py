import networkx as nx
import Setting_Simulation_Value
import InterconnectedLayerModeling
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import operator


class CalculatingProperty:

    def making_df_for_property(self, panda_df, inter_layer, node_i_name):
        i = int(node_i_name.split('_')[1])
        panda_df['A_Clustering'] = self.cal_clustering(inter_layer)[i]
        panda_df['A_Hub'] = self.cal_hub_and_authority(inter_layer)[0][i]
        panda_df['A_Authority'] = self.cal_hub_and_authority(inter_layer)[1][i]
        panda_df['A_Pagerank'] = self.cal_pagerank(inter_layer)[i]
        panda_df['A_Eigenvector'] = self.cal_eigenvector_centrality(inter_layer)[i]
        panda_df['A_Degree'] = self.cal_degree_centrality(inter_layer)[i]
        panda_df['A_Betweenness'] = self.cal_betweenness_centrality(inter_layer)[i]
        panda_df['A_Closeness'] = self.cal_closeness_centrality(inter_layer)[i]
        panda_df['A_Load'] = self.cal_load_centrality(inter_layer)[i]
        connected_B_node = self.finding_B_node(inter_layer, i)
        panda_df['Connected_B_node'] = connected_B_node
        panda_df['B_Clustering'] = self.cal_clustering(inter_layer)[connected_B_node]
        panda_df['B_Hub'] = self.cal_hub_and_authority(inter_layer)[0][connected_B_node]
        panda_df['B_Authority'] = self.cal_hub_and_authority(inter_layer)[1][connected_B_node]
        panda_df['B_Pagerank'] = self.cal_pagerank(inter_layer)[connected_B_node]
        panda_df['B_Eigenvector'] = self.cal_eigenvector_centrality(inter_layer)[connected_B_node]
        panda_df['B_Degree'] = self.cal_degree_centrality(inter_layer)[connected_B_node]
        panda_df['B_Betweenness'] = self.cal_betweenness_centrality(inter_layer)[connected_B_node]
        panda_df['B_Closeness'] = self.cal_closeness_centrality(inter_layer)[connected_B_node]
        panda_df['B_Load'] = self.cal_load_centrality(inter_layer)[connected_B_node]
        return panda_df

    def finding_B_node(self, inter_layer, i):
        connected_B_node = 0
        neighbors = sorted(nx.neighbors(inter_layer.two_layer_graph, i))
        for neighbor in neighbors:
            if neighbor > (len(sorted(inter_layer.A_edges))-1):
                connected_B_node = neighbor
        return connected_B_node

    def cal_clustering(self, inter_layer):
        clustering = nx.clustering(inter_layer.two_layer_graph)
        return clustering     # value = clustering[node_number]

    def cal_hub_and_authority(self, inter_layer):
        hub, authority = nx.hits(inter_layer.two_layer_graph)
        return hub, authority  # value = hub[node_number]
        # hub_order = sorted(h.items(), key=operator.itemgetter(1), reverse=True)
        # authority_order = sorted(a.items(), key=operator.itemgetter(1), reverse=True)

    def cal_pagerank(self, inter_layer):
        pagerank = nx.pagerank(inter_layer.two_layer_graph)
        return pagerank  # value = pagerank[node_number]

    def cal_eigenvector_centrality(self, inter_layer):
        eigenvector_centrality = nx.eigenvector_centrality(inter_layer.two_layer_graph)
        return eigenvector_centrality

    def cal_degree_centrality(self, inter_layer):
        degree_centrality = nx.degree_centrality(inter_layer.two_layer_graph)
        return degree_centrality

    def cal_betweenness_centrality(self, inter_layer):
        betweenness_centrality = nx.betweenness_centrality(inter_layer.two_layer_graph)
        return betweenness_centrality

    def cal_closeness_centrality(self, inter_layer):
        closeness_centrality = nx.closeness_centrality(inter_layer.two_layer_graph)
        return closeness_centrality

    def cal_load_centrality(self, inter_layer):
        load_centrality = nx.load_centrality(inter_layer.two_layer_graph)
        return load_centrality

if __name__ == "__main__":
    print("CalculatingProperty")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    cal_property = CalculatingProperty()



