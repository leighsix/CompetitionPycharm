from pymnet import *
import matplotlib.pyplot as plt
import Setting_Simulation_Value
import InterconnectedLayerModeling
from mpl_toolkits.mplot3d.axes3d import *
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.image import imread
import matplotlib
matplotlib.use("TkAgg")


class Interconnected_Network_Visualization:
    def making_layer_A_graph(self, setting, inter_layer, interconnected_network):
        interconnected_network.add_layer('layer_A')
        for i in range(setting.A_node):
            interconnected_network.add_node(i)
        for i, j in sorted(inter_layer.A_edges.edges):
            interconnected_network[i, j, 'layer_A'] = 1
        return interconnected_network

    def making_layer_B_graph(self, setting, inter_layer, interconnected_network):
        interconnected_network.add_layer('layer_B')
        for i in range(setting.B_node):
            interconnected_network.add_node(i)
        for i, j in sorted(inter_layer.B_edges):
            interconnected_network[i-setting.A_node, j-setting.A_node, 'layer_B'] = 1
        return interconnected_network

    def making_interconnected_layer(self, setting, inter_layer):
        interconnected_network = MultilayerNetwork(aspects=1)
        self.making_layer_A_graph(setting, inter_layer, interconnected_network)
        self.making_layer_B_graph(setting, inter_layer, interconnected_network)
        for i, j in sorted(inter_layer.AB_edges):
            interconnected_network[j, 'layer_A'][i-setting.A_node, 'layer_B'] = 1
        return interconnected_network

    def making_node_color(self, setting, inter_layer):
        node_color_dic = {}
        for i in range(setting.A_node):
            node_color_dic[(i, 'layer_A')] = setting.NodeColorDict[inter_layer.two_layer_graph.nodes[i]['state']]
        for i in range(setting.B_node):
            node_color_dic[(i, 'layer_B')] = setting.NodeColorDict[inter_layer.two_layer_graph.nodes[i+setting.A_node]['state']]
        return node_color_dic

    def making_edge_color(self, setting, inter_layer):
        edge_color_dic = {}
        for i, j in sorted(inter_layer.A_edges.edges):
            a = inter_layer.two_layer_graph.nodes[i]['state']
            b = inter_layer.two_layer_graph.nodes[j]['state']
            edge_color_dic[(i, 'layer_A'), (j, 'layer_A')] = setting.EdgeColorDict[a * b]
        for i, j in sorted(inter_layer.B_edges):
            a = inter_layer.two_layer_graph.nodes[i]['state']
            b = inter_layer.two_layer_graph.nodes[j]['state']
            edge_color_dic[(i-setting.A_node, 'layer_B'), (j-setting.A_node, 'layer_B')] = setting.EdgeColorDict[a * b]
        for i, j in sorted(inter_layer.AB_edges):
            a = inter_layer.two_layer_graph.nodes[j]['state']
            b = inter_layer.two_layer_graph.nodes[i]['state']
            edge_color_dic[(j-setting.A_node, 'layer_A'), (i, 'layer_B')] = setting.EdgeColorDict[a * b]
        return edge_color_dic

    def making_node_coordinates(self, setting, inter_layer):
        node_coordinates_dic = {}
        for i in range(setting.A_node):
            node_coordinates_dic[i] = np.array(inter_layer.A_node_info['location'][i])
        for i in range(setting.B_node):
            node_coordinates_dic[i] = np.array(inter_layer.B_node_info['location'][i])
        return node_coordinates_dic

    def draw_interconnected_network(self, setting, inter_layer, save_file_name):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        draw(self.making_interconnected_layer(setting, inter_layer), layout='circular', layergap=1.3,
             layershape='rectangle', nodeCoords=self.making_node_coordinates(setting, inter_layer), nodelayerCoords={},
             layerPadding=0.05, alignedNodes=True, ax=ax, layerColorDict={'layer_A': 'pink', 'layer_B': 'steelblue'},
             layerColorRule={}, edgeColorDict = self.making_edge_color(setting, inter_layer), edgeColorRule={},
             edgeWidthDict={}, edgeWidthRule={}, defaultEdgeWidth=0.15, edgeStyleDict={},
             edgeStyleRule={'rule': 'edgetype', 'inter': ':', 'intra': '-'}, defaultEdgeStyle='-',
             nodeLabelDict={}, nodeLabelRule={}, defaultNodeLabel=None,
             nodeColorDict=self.making_node_color(setting, inter_layer), nodeColorRule={}, defaultNodeColor=None,
             nodeLabelColorDict={}, nodeLabelColorRule={}, defaultNodeLabelColor='k',
             nodeSizeDict={}, nodeSizeRule={'scalecoeff': 0.2, 'rule': 'scaled'}, defaultNodeSize=None)
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
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    ILM = Interconnected_Network_Visualization()
    fig = ILM.draw_interconnected_network(setting, inter_layer, 'result.png')[1]
    plt.show()
    print("Operating finished")
