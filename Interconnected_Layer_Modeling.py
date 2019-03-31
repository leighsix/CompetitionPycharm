from pymnet import *
import matplotlib.pyplot as plt
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling
from mpl_toolkits.mplot3d.axes3d import *
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.image import imread
import matplotlib
matplotlib.use("TkAgg")


class Interconnected_Layer_Modeling:
    def making_layer_A_graph(self, layer_A, interconnected_network):
        interconnected_network.add_layer('layer_A')
        for i in sorted(layer_A.G_A.nodes):
            interconnected_network.add_node(i)
        for i, j in sorted(layer_A.G_A.edges):
            interconnected_network[i, j, 'layer_A'] = 1
        return interconnected_network

    def making_layer_B_graph(self, layer_B, interconnected_network):
        interconnected_network.add_layer('layer_B')
        for i in sorted(layer_B.G_B.nodes):
            interconnected_network.add_node(i)
        for i, j in sorted(layer_B.G_B.edges):
            interconnected_network[i, j, 'layer_B'] = 1
        return interconnected_network

    def making_interconnected_layer(self, layer_A, layer_B):
        interconnected_network = MultilayerNetwork(aspects=1)
        self.making_layer_A_graph(layer_A, interconnected_network)
        self.making_layer_B_graph(layer_B, interconnected_network)
        for i, j in sorted(layer_A.AB_edges):
            interconnected_network[j, 'layer_A'][i, 'layer_B'] = 1
        return interconnected_network

    def making_node_color(self, setting, layer_A, layer_B):
        node_color_dic = {}
        for i in sorted(layer_A.G_A.nodes):
            node_color_dic[(i, 'layer_A')] = setting.NodeColorDict[layer_A.G_A.nodes[i]['state']]
        for i in sorted(layer_B.G_B.nodes):
            node_color_dic[(i, 'layer_B')] = setting.NodeColorDict[layer_B.G_B.nodes[i]['state']]
        return node_color_dic

    def making_edge_color(self, setting, layer_A, layer_B):
        edge_color_dic = {}
        for i, j in sorted(layer_A.G_A.edges):
            a = layer_A.G_A.nodes[i]['state']
            b = layer_A.G_A.nodes[j]['state']
            edge_color_dic[(i, 'layer_A'), (j, 'layer_A')] = setting.EdgeColorDict[a * b]
        for i, j in sorted(layer_B.G_B.edges):
            a = layer_B.G_B.nodes[i]['state']
            b = layer_B.G_B.nodes[j]['state']
            edge_color_dic[(i, 'layer_B'), (j, 'layer_B')] = setting.EdgeColorDict[a * b]
        for i, j in sorted(layer_A.AB_edges):
            a = layer_A.G_A.nodes[j]['state']
            b = layer_B.G_B.nodes[i]['state']
            edge_color_dic[(j, 'layer_A'), (i, 'layer_B')] = setting.EdgeColorDict[a * b]
        return edge_color_dic

    def making_node_coordinates(self, layer_A, layer_B):
        node_coordinates_dic = {}
        for i in sorted(layer_A.G_A.nodes):
            node_coordinates_dic[i] = np.array(layer_A.A_node_info['location'][i])
        for i in sorted(layer_B.G_B.nodes):
            node_coordinates_dic[i] = np.array(layer_B.B_node_info['location'][i])
        return node_coordinates_dic

    def draw_interconnected_network(self, setting, layer_A, layer_B, save_file_name):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        draw(self.making_interconnected_layer(layer_A, layer_B), layout='circular', layergap=1.3,
             layershape='rectangle', nodeCoords=self.making_node_coordinates(layer_A, layer_B), nodelayerCoords={},
             layerPadding=0.05, alignedNodes=True, ax=ax, layerColorDict={'layer_A': 'pink', 'layer_B': 'steelblue'},
             layerColorRule={}, edgeColorDict = self.making_edge_color(setting, layer_A, layer_B), edgeColorRule={},
             edgeWidthDict={}, edgeWidthRule={}, defaultEdgeWidth=0.01, edgeStyleDict={},
             edgeStyleRule={'rule': 'edgetype', 'inter': ':', 'intra': '-'}, defaultEdgeStyle='-',
             nodeLabelDict={}, nodeLabelRule={}, defaultNodeLabel=None,
             nodeColorDict=self.making_node_color(setting, layer_A, layer_B), nodeColorRule={}, defaultNodeColor=None,
             nodeLabelColorDict={}, nodeLabelColorRule={}, defaultNodeLabelColor='k',
             nodeSizeDict={}, nodeSizeRule={'scalecoeff': 0.1, 'rule': 'scaled'}, defaultNodeSize=None)
        plt.savefig(save_file_name)
        im = plt.imread(save_file_name)
        return np.array(im), fig

    def making_movie_for_dynamics(self, ims):
        dpi = 72
        x_pixels, y_pixels = ims[0].shape[0], ims[0].shape[1]
        fig = plt.figure(figsize=(y_pixels / dpi, x_pixels / dpi), dpi=dpi)
        im = plt.figimage(ims[0])

        def animate(i):
            im.set_array(ims[i])
            return (im,)
        ani = animation.FuncAnimation(fig, animate, frames=len(ims), repeat=False, interval=1000)
        ani.save('dynamics2.mp4')


if __name__ == "__main__":
    print("Interconnected Layer Modeling")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    ILM = Interconnected_Layer_Modeling()
    fig = ILM.draw_interconnected_network(setting, layer_A, layer_B, 'result.png')[1]
    plt.show()
    print("Operating finished")
