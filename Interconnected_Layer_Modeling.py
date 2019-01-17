from pymnet import *
import matplotlib.pyplot as plt
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling
from mpl_toolkits.mplot3d.axes3d import *
from PIL import Image
import matplotlib.animation as animation


class Interconnected_Layer_Modeling:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def making_layer_A_graph(self, layer_A, interconnected_network):
        interconnected_network.add_layer('layer_A')
        for i in sorted(layer_A.A_edges.nodes):
            interconnected_network.add_node(i)
        for i, j in sorted(layer_A.A_edges.edges):
            interconnected_network[i, j, 'layer_A'] = 1
        return interconnected_network

    def making_layer_B_graph(self, layer_B, interconnected_network):
        interconnected_network.add_layer('layer_B')
        for i in sorted(layer_B.B_edges.nodes):
            interconnected_network.add_node(i)
        for i, j in sorted(layer_B.B_edges.edges):
            interconnected_network[i, j, 'layer_B'] = 1
        return interconnected_network

    def making_interconnected_layer(self, layer_A, layer_B):
        interconnected_network = MultilayerNetwork(aspects=1)
        self.making_layer_A_graph(layer_A, interconnected_network)
        self.making_layer_B_graph(layer_B, interconnected_network)
        for i, j in sorted(layer_A.AB_edges):
            interconnected_network[j, 'layer_A'][i, 'layer_B'] = 1
        return interconnected_network

    def making_node_color(self, layer_A, layer_B):
        node_color_dic = {}
        for i in sorted(layer_A.A_edges.nodes):
            node_color_dic[(i, 'layer_A')] = self.SS.NodeColorDict[layer_A.A[i]]
        for i in sorted(layer_B.B_edges.nodes):
            node_color_dic[(i, 'layer_B')] = self.SS.NodeColorDict[layer_B.B[i]]
        return node_color_dic

    def making_edge_color(self, layer_A, layer_B):
        edge_color_dic = {}
        for i, j in sorted(layer_A.A_edges.edges):
            edge_color_dic[(i, 'layer_A'), (j, 'layer_A')] = self.SS.EdgeColorDict[layer_A.A[i]*layer_A.A[j]]
        for i, j in sorted(layer_B.B_edges.edges):
            edge_color_dic[(i, 'layer_B'), (j, 'layer_B')] = self.SS.EdgeColorDict[layer_B.B[i]*layer_B.B[j]]
        for i, j in sorted(layer_A.AB_edges):
            edge_color_dic[(j, 'layer_A'), (i, 'layer_B')] = self.SS.EdgeColorDict[layer_A.A[j]*layer_B.B[i]]
        return edge_color_dic

    def making_node_coordinates(self, layer_A, layer_B):
        node_coordinates_dic = {}
        for i in sorted(layer_A.A_edges.nodes):
            node_coordinates_dic[i] = np.array(layer_A.A_node_info['location'][i])
        for i in sorted(layer_B.B_edges.nodes):
            node_coordinates_dic[i] = np.array(layer_B.B_node_info['location'][i])
        return node_coordinates_dic

    def draw_interconnected_network(self, layer_A, layer_B, save_file_name):
        ax = plt.axes(projection='3d')
        draw(self.making_interconnected_layer(layer_A, layer_B), layout='circular', layergap=1.3,
             layershape='rectangle', nodeCoords=self.making_node_coordinates(layer_A, layer_B), nodelayerCoords={},
             layerPadding=0.05, alignedNodes=True, ax=ax, layerColorDict={'layer_A': 'pink', 'layer_B': 'steelblue'},
             layerColorRule={}, edgeColorDict = self.making_edge_color(layer_A, layer_B), edgeColorRule={},
             edgeWidthDict={}, edgeWidthRule={}, defaultEdgeWidth=0.01, edgeStyleDict={},
             edgeStyleRule={'rule': 'edgetype', 'inter': ':', 'intra': '-'}, defaultEdgeStyle='-',
             nodeLabelDict={}, nodeLabelRule={}, defaultNodeLabel=None,
             nodeColorDict=self.making_node_color(layer_A, layer_B), nodeColorRule={}, defaultNodeColor=None,
             nodeLabelColorDict={}, nodeLabelColorRule={}, defaultNodeLabelColor='k',
             nodeSizeDict={}, nodeSizeRule={'scalecoeff': 0.1, 'rule': 'scaled'}, defaultNodeSize=None)
        plt.savefig(save_file_name)
        img = Image.open(save_file_name)
        im = plt.imshow(img)
        return im

    def making_movie_for_dynamics(self, ims):
        fig = plt.figure()
        ani = animation.ArtistAnimation(fig, ims, interval=10, blit=True)
        ani.save('dynamics.mp4')


if __name__ == "__main__":
    print("Interconnected Layer Modeling")
    layer_A = Layer_A_Modeling.Layer_A_Modeling()
    layer_B = Layer_B_Modeling.Layer_B_Modeling()
    ILM = Interconnected_Layer_Modeling()
    ILM.draw_interconnected_network(layer_A, layer_B, 'result3')
    print("Operating finished")
