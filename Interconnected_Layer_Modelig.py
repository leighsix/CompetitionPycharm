from pymnet import *
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling


class Interconnected_Layer_Modeling:
    def __init__(self):
        self.SS = Setting_Simulation_Value

    def making_layer_A_graph(self, layer_A, interconnected_network):
        interconnected_network.add_layer('layer_A')
        for i in sorted(layer_A.A_edges.nodes):
            interconnected_network.add_node(i)
        for i, j in sorted(layer_A.A_edges.edges):
            interconnected_network[i, j, 'layer_A'] = 1

    def making_layer_B_graph(self, layer_B, interconnected_network):
        interconnected_network.add_layer('layer_B')
        for i in sorted(layer_B.B_edges.nodes):
            interconnected_network.add_node(i)
        for i, j in sorted(layer_B.B_edges.edges):
            interconnected_network[i, j, 'layer_B'] = 1


    def making_interconnected_layer(self, layer_A, layer_B):
        interconnected_network = MultilayerNetwork(aspects=1)
        self.making_layer_A_graph(layer_A, interconnected_network)
        self.making_layer_B_graph(layer_B, interconnected_network)
        for i, j in sorted(layer_A.AB_edges):
            interconnected_network[j, 'layer_A'][i, 'layer_B'] = 1
        return interconnected_network


if __name__ == "__main__":
    print("Interconnected Layer Modeling")
    layer_A = Layer_A_Modeling.Layer_A_Modeling()
    layer_B = Layer_B_Modeling.Layer_B_Modeling()
    ILM = Interconnected_Layer_Modeling()
    result = ILM.making_interconnected_layer(layer_A, layer_B)
    fig = draw(result, layout='spring', show=False, layergap=1.3, layerPadding=0.05, alignedNodes=True, ax=None,
               layerColorDict={'layer_A': 'pink', 'layer_B': 'steelblue'}, layerColorRule={}, defaultLayerColor='#29b7c1',
               edgeWidthDict={}, edgeWidthRule={}, defaultEdgeWidth=0.05,
               edgeStyleDict={}, edgeStyleRule={'inter': ':', 'intra': '-', 'rule': 'edgetype'}, defaultEdgeStyle='-',
               nodeLabelDict= {}, nodeLabelRule={}, defaultNodeLabel=None,
               nodeLabelColorDict = {} ,nodeLabelColorRule={}, defaultNodeLabelColor='k',
               nodeSizeDict={}, nodeSizeRule={'scalecoeff': 0.3, 'rule': 'scaled'}, defaultNodeSize=None)
    fig.savefig('result')
    print("Operating finished")
