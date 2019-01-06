def AS_model_function(a):  # B layer 에서 일어나는 변동 현상
    z = random.random()
    if z < prob_beta:
        a = -a
    return a