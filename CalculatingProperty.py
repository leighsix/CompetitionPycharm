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

    def making_df_for_property(self, panda_df, inter_layer, i):
        panda_df['Clustering'] = self.cal_clustering(inter_layer)[i]
        panda_df['Hub'] = self.cal_hub_and_authority(inter_layer)[0][i]
        panda_df['Authority'] = self.cal_hub_and_authority(inter_layer)[1][i]
        panda_df['Pagerank'] = self.cal_pagerank(inter_layer)[i]
        panda_df['Eigenvector'] = self.cal_eigenvector_centrality(inter_layer)[i]
        panda_df['Degree'] = self.cal_degree_centrality(inter_layer)[i]
        panda_df['Betweenness'] = self.cal_betweenness_centrality(inter_layer)[i]
        panda_df['Closeness'] = self.cal_closeness_centrality(inter_layer)[i]
        panda_df['Load'] = self.cal_load_centrality(inter_layer)[i]
        return panda_df


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
    df = cal_property.making_df_for_property(inter_layer, 0)
    print(df)
    # df = cal_property.making_df_for_property(inter_layer, 1)
    # print(df)



