
def A_layer_persuasion_function(a, b):  # A layer 중에서 same orientation 에서 일어나는  변동 현상
    z = random.random()
    if z < prob_p:
        if a > 0:
            a = A_layer_node_right(a, MAX)
            b = A_layer_node_right(b, MAX)
        elif a < 0:
            a = A_layer_node_left(a, MIN)
            b = A_layer_node_left(b, MIN)
    elif z > prob_p:
        a = a
        b = b
    return a, b


def A_layer_node_left(a, MIN):
    if a >= MIN:
        if a == MIN:
            a = a
        elif a < 0 or a > 1:
            a = a - 1
        elif a == 1:
            a = -1
    elif a < MIN:
        a = MIN
    return a


def A_layer_node_right(a, MAX):
    if a <= MAX:
        if a == MAX:
            a = a
        elif a > 0 or a < -1:
            a = a + 1
        elif a == -1:
            a = 1
    elif a > MAX:
        a = MAX
    return a


def A_layer_compromise_function(a, b):  # A layer  중에서 opposite orientation 에서 일어나는 변동 현상
    z = random.random()
    if z < (1 - prob_p):
        if a * b == -1:
            if z < ((1 - prob_p) / 2):
                a = 1
                b = 1
            elif z > ((1 - prob_p) / 2):
                a = -1
                b = -1
        elif a > b:
            a = A_layer_node_left(a, MIN)
            b = A_layer_node_right(b, MAX)
        elif a < b:
            a = A_layer_node_right(a, MAX)
            b = A_layer_node_left(b, MIN)
    elif z > (1 - prob_p):
        a = a
        b = b
    return a, b


def AB_layer_persuasion_function(a, b):  # A-B layer 중에서 same orientation 에서 일어나는  변동 현상
    z = random.random()
    if z < prob_p:
        if a > 0:
            a = A_layer_node_right(a, MAX)
            b = b
        elif a < 0:
            a = A_layer_node_left(a, MIN)
            b = b
    elif z > prob_p:
        a = a
        b = b
    return a, b


def AB_layer_compromise_function(a, b):  # A-B layer  중에서 opposite orientation 에서 일어나는 변동 현상
    z = random.random()
    if z < (1 - prob_p):
        if a * b == -1:
            if z < ((1 - prob_p) / 2):
                a = 1
                b = b
            elif z > ((1 - prob_p) / 2):
                a = -1
                b = b
        elif a > b:
            a = A_layer_node_left(a, MIN)
            b = b
        elif a < b:
            a = A_layer_node_right(a, MAX)
            b = b
    elif z > (1 - prob_p):
        a = a
        b = b
    return a, b