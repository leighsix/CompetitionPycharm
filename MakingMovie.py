import Setting_Simulation_Value
from pymnet import *
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from matplotlib import animation
from sympy import *
import Layer_A_Modeling
import Layer_B_Modeling


class MakingMovie:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def making_A_layer_graph():
        global A_pair, A_nodecolor
        A_pair = []
        A_nodecolor = []
        inter_net.add_layer('A_layer')
        for i in sorted(A_edges.nodes):
            inter_net.add_node(i)
            if layer_A.A[i] == 2:
                A_nodecolor.append((i, 'A_layer', 2))
            elif layer_A.A[i] == 1:
                A_nodecolor.append((i, 'A_layer', 1))
        for i, j in sorted(A_edges.edges):
            inter_net[i, j, 'A_layer'] = 1
            A_pair.append(((i, 'A_layer'), (j, 'A_layer')))
        return inter_net
      # "rule":"edgeweight","colormap":"jet","scaleby":0.1

    def making_B_layer_graph():
        global B_pair, B_nodecolor
        B_pair = []
        B_nodecolor = []
        inter_net.add_layer('B_layer')
        for i in sorted(B_edges.nodes):
            inter_net.add_node(i)
            if B[i] == 1:
                B_nodecolor.append((i, 'B_layer', 1))
            elif B[i] == -1:
                B_nodecolor.append((i, 'B_layer', -1))
        for i, j in sorted(B_edges.edges):
            inter_net[i, j, 'B_layer'] = 1
            B_pair.append(((i, 'B_layer'), (j, 'B_layer')))
        return inter_net

    def inter_edge_graph():
        global inter_pair, inter_net
        inter_pair = []
        inter_net = MultilayerNetwork(aspects=1)
        making_A_layer_graph()
        making_B_layer_graph()
        for i, j in sorted(AB_edges):
            inter_net[j, 'A_layer'][i, 'B_layer'] = 1
            inter_pair.append(((j, 'A_layer'), (i, 'B_layer')))
        return inter_net

    def edgecolordic():
        global edgeColorDict
        edgeColorDict = {}
        for i in range(int(len(A_edges.edges))):
            edgeColorDict[A_pair[i]] = 'r'
        for i in range(int(len(B_edges.edges))):
            edgeColorDict[B_pair[i]] = 'b'
        for i in range(int(len(AB_edges))):
            edgeColorDict[inter_pair[i]] = 'g'
        return edgeColorDict

    ## nodeColorDict={(0,0):"r",(1,0):"r",(0,1):"r"}

    def nodecolordic():
        global nodeColorDict
        nodeColorDict = {}
        for i in range(int(len(A_nodecolor))):
            if A_nodecolor[i][2] == 2:
                nodeColorDict[(A_nodecolor[i][0], 'A_layer')] = 'red'
            elif A_nodecolor[i][2] == 1:
                nodeColorDict[(A_nodecolor[i][0], 'A_layer')] = 'hotpink'
            elif A_nodecolor[i][2] == -1:
                nodeColorDict[(A_nodecolor[i][0], 'A_layer')] = 'deepskyblue'
            elif A_nodecolor[i][2] == -2:
                nodeColorDict[(A_nodecolor[i][0], 'A_layer')] = 'blue'
        for i in range(int(len(B_nodecolor))):
            if B_nodecolor[i][2] == 1:
                nodeColorDict[(B_nodecolor[i][0], 'B_layer')] = 'hotpink'
            elif B_nodecolor[i][2] == -1:
                nodeColorDict[(B_nodecolor[i][0], 'B_layer')] = 'deepskyblue'
        return nodeColorDict

    def nodecoordsdic():
        global nodeCoordsDict
        nodeCoordsDict = {}
        for i in sorted(A_edges.nodes):
            nodeCoordsDict[i, 'A_layer'] = ((1 / (i + 1)), 0.9)
        for i in sorted(B_edges.nodes):
            nodeCoordsDict[i, 'B_layer'] = ((1 / (i + 1)), 0.1)
        return nodeCoordsDict

    def nodelayercoordsdic():
        global nodelayerCoordsDict
        nodelayerCoordsDict = {'A_layer': (1, 1), 'B_layer': (0, 0)}
        return nodelayerCoordsDict

    def drawing_graph(result):  # drawing_graph("inter_net_BA_leaderasdf.png")
        inter_edge_graph()
        fig = draw(inter_net, layout='spring', show=False, layergap=1.3,
                   nodeCoords=nodecoordsdic(), nodelayerCoords=nodelayercoordsdic(),
                   layerPadding=0.05, alignedNodes=True, ax=None,
                   layerColorDict={'A_layer': 'pink', 'B_layer': 'steelblue'}, layerColorRule={},
                   defaultLayerColor='#29b7c1',
                   edgeColorDict=edgecolordic(),
                   edgeWidthDict={}, edgeWidthRule={}, defaultEdgeWidth=0.05,
                   edgeStyleDict={}, edgeStyleRule={'inter': ':', 'intra': '-', 'rule': 'edgetype'},
                   defaultEdgeStyle='-',
                   nodeLabelDict={}, nodeLabelRule={}, defaultNodeLabel=None,
                   nodeColorDict=nodecolordic(), nodeColorRule={}, defaultNodeColor=None,
                   nodeLabelColorDict={}, nodeLabelColorRule={}, defaultNodeLabelColor='k',
                   nodeSizeDict={}, nodeSizeRule={'scalecoeff': 0.3, 'rule': 'scaled'}, defaultNodeSize=None)
        fig.savefig(result)
        image = plt.imread(result)
        return image

    def animation_interconnected_dynamics(result):
        A_layer_dynamics()
        B_layer_dynamics()
        drawing_graph(result)
        return drawing_graph(result)

    def plot_movie_mp4(image_array, result):
        dpi = 72.0
        xpixels, ypixels = image_array[0].shape[0], image_array[0].shape[1]
        fig = plt.figure(figsize=(ypixels / dpi, xpixels / dpi), dpi=dpi)
        im = plt.figimage(image_array[0])

        def animate(i):
            im.set_array(image_array[i])
            return (im,)

        anim = animation.FuncAnimation(fig, animate, frames=len(image_array), repeat=False, interval=500)
        anim.save(result)
        display(HTML(anim.to_html5_video()))


if __name__ == "__main__":
    print("Making the movie for competition")
    making_interconnected_edges()
    static_variable(0.5, 2)
    fig = plt.figure()
    ims = [np.array(drawing_graph('dynamic_image.png'))]
    limited_time = 1000
    total = 0
    while True:
        im = animation_interconnected_dynamics('dynamic_image.png')
        ims.append(np.array(im))
        total += 1
        if (np.all(A > 0) == 1 and np.all(B > 0) == 1) or (np.all(A < 0) == 1 and np.all(B < 0) == 1) or (
                total == limited_time):
            break
    im = animation_interconnected_dynamics('dynamic_image.png')
    ims.append(np.array(im))
    IMS = np.array(ims)
    plot_movie_mp4(IMS, 'dynamic_images_no_leader(128（BA), 128(RR), ganma=0.5, beta=2).mp4')
