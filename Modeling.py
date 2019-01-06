class interconnected_A_layer_modeling:
    def __init__(self, state, node, edge, Max, Min,
                 network):  # network : 1 = random regular graph   2 = barabasi-albert graph
        self.state = state
        self.node = node
        self.edge = edge
        self.Max = Max
        self.Min = Min
        self.network = network

    def A_layer_config(self):  # A_layer 구성요소 A_layer_config(state = [1,2], node = 2048, edge = 5, Max = 2, Min = -2)
        global A_state, A_node, A_edge, MAX, MIN
        A_state = self.state  # state = [   ]  kinds of states
        A_node = self.node
        A_edge = self.edge
        MAX = self.Max
        MIN = self.Min
        return A_state, A_node, A_edge, MAX, MIN

    def select_layer_A_model(self):
        network = self.network
        if network == 1:
            making_layer_A_random_regular()
        elif network == 2:
            making_layer_A_barabasi_albert()
        return A, A_edges, MAX, MIN


def making_layer_A_random_regular():  # A_layer random_regular network
    global A, A_edges
    A = np.array(A_state * int(A_node / len(A_state)), int)
    random.shuffle(A)
    A_edges = nx.random_regular_graph(A_edge, A_node, seed=None)
    return A, A_edges, MAX, MIN


def making_layer_A_barabasi_albert():  # A_layer 바바라시-알버트 네트워크
    global A, A_edges
    A = np.array(A_state * int(A_node / len(A_state)), int)
    random.shuffle(A)
    A_edges = nx.barabasi_albert_graph(A_node, A_edge, seed=None)
    return A, A_edges, MAX, MIN


class interconnected_B_layer_modeling:
    def __init__(self, state, node, edge, inter_edges,
                 network):  # network : 1 = random regular graph   2 = barabasi-albert graph
        self.state = state
        self.node = node
        self.edge = edge
        self.inter_edges = inter_edges
        self.network = network

    def B_layer_config(self):  # B_layer 구성요소 B_layer_config(state = [-1], node = 2048, edge = 5, inter_edge= 1)
        global B_state, B_node, B_edge, inter_edges
        B_state = self.state  # state = [   ]  kinds of states
        B_node = self.node
        B_edge = self.edge
        inter_edges = self.inter_edges
        return B_state, B_node, B_edge, inter_edges

    def select_layer_B_model(self):
        network = self.network
        if network == 1:
            making_layer_B_random_regular()
        elif network == 2:
            making_layer_B_barabasi_albert()
        return B, B_edges

    def making_interconnected_edges(self):  #
        global AB_edges, AB_neighbor
        inter_edges = self.inter_edges
        AB_edges = []
        AB_neighbor = []
        for i in range(int(A_node / inter_edges)):
            for j in range(inter_edges):
                connected_A_node = np.array(A_edges.nodes).reshape(-1, inter_edges)[i][j]
                AB_neighbor.append(connected_A_node)
                AB_edges.append((i, connected_A_node))
        AB_neighbor = np.array(AB_neighbor).reshape(-1, inter_edges)
        return AB_edges, AB_neighbor


def making_layer_B_random_regular():  # B_layer random_regular network
    global B, B_edges
    B = np.array(B_state * int(B_node / len(B_state)), int)
    random.shuffle(B)
    B_edges = nx.random_regular_graph(B_edge, B_node, seed=None)
    return B, B_edges


def making_layer_B_barabasi_albert():  # B_layer 바바라시-알버트 네트워크
    global B, B_edges
    B = np.array(B_state * int(B_node / len(B_state)), int)
    random.shuffle(B)
    B_edges = nx.barabasi_albert_graph(B_node, B_edge, seed=None)
    return B, B_edges

def making_beta_scale(a):
    scale = math.log((1 / (B_edge + 1)) ** 3) / math.log(inter_edges / (B_edge + inter_edges))
    return (0, scale, a)


def simulation_condition(ganma_scale, beta_scale, Repeating_number, Limited_time):
    global r, D, repeating_number, limited_time
    r = np.linspace(ganma_scale[0], ganma_scale[1], ganma_scale[2])
    D = np.linspace(beta_scale[0], beta_scale[1], beta_scale[2])
    repeating_number = Repeating_number  # 평균을 내기위한 반복 횟수
    limited_time = Limited_time  # layer 변화를 위한 반복 횟수
    return r, D, repeating_number, limited_time





