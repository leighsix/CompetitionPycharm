from IPython.display import display
from sympy import *
import numpy as np
import OpinionDynamics
import DecisionDynamics
import Visualization
import MakingMovie
import Modeling

Modeling


class Competition:
    def __init__(self):
        self.modeling = Modeling.Modeling()
        self.opinion_dynamics = OpinionDynamics.OpinionDynamics()
        self.decision_dynamics = DecisionDynamics.DecisionDynamics()
        self.visualization = Visualization.Visualization()
        self.makingDB = MakingMovie.MakingDB()




def fraction_different_state():
    global A_layer_fraction, B_layer_fraction
    A_plus = sum(A > 0)
    A_minus = sum(A < 0)
    if A_plus >= A_minus:
        A_layer_fraction = min(A_plus, A_minus) / len(A)
    elif A_plus < A_minus:
        A_layer_fraction = -(min(A_plus, A_minus)) / len(A)
    B_plus = sum(B > 0)
    B_minus = sum(B < 0)
    if B_plus >= B_minus:
        B_layer_fraction = min(B_plus, B_minus) / len(B)
    elif B_plus < B_minus:
        B_layer_fraction = -(min(B_plus, B_minus)) / len(B)
    return A_layer_fraction, B_layer_fraction








def interconnected_dynamics():
    global Probability_plus, passtime, B_plus, A_plus, Flow_prob_beta, Flow_Prob_Beta, Fraction_A_state, Fraction_B_state, fraction_A_layer, fraction_B_layer

    starttime = time.time()  # 시간 측정
    Flow_prob_beta = []  # 노드의 prob_beta 평균에 대한 변화 리스트
    Flow_Prob_Beta = pd.DataFrame()  # prob_beta 평균의 변화를 칼럼으로 정리
    fraction_A_state = []  # A_layer의 different state 비율
    fraction_B_state = []  # B_layer의 different state 비율
    Fraction_A_state = pd.DataFrame()  # A_layer의 different state 비율(데이터프레임)
    Fraction_B_state = pd.DataFrame()  # B_layer의 different state 비율(데이터프레임)
    Probability_plus = 0  # +로 consensus 되는 확률 측정
    total = 0
    while True:
        A_layer_dynamics()
        B_layer_dynamics()
        fraction_different_state()
        total += 1
        fraction_A_state.append(A_layer_fraction)
        fraction_B_state.append(B_layer_fraction)
        if (np.all(A > 0) == 1 and np.all(B > 0) == 1) or (np.all(A < 0) == 1 and np.all(B < 0) == 1) or (
                total == limited_time):
            break
    endtime = time.time()
    passtime = endtime - starttime
    Flow_Prob_Beta = pd.DataFrame(Flow_prob_beta)  # prob_beta 평균의 변화를 칼럼으로 정리
    Fraction_A_state = pd.DataFrame(fraction_A_state)  # prob_beta 평균의 변화를 칼럼으로 정리
    Fraction_B_state = pd.DataFrame(fraction_B_state)  # prob_beta 평균의 변화를 칼럼으로 정리
    if np.all(A > 0) == 1 and np.all(B > 0) == 1:
        Probability_plus += 1
    elif np.all(A < 0) == 1 and np.all(B < 0) == 1:
        Probability_plus += 0
    elif total == limited_time:
        Probability_plus += 0
    B_plus = sum(B)  # B_layer 노드의 합
    A_plus = sum(A)  # A_layer 노드의 합
    fraction_A_layer = (sum(A > 0) / len(A))
    fraction_B_layer = (sum(B > 0) / len(B))
    return A, B, A_plus, B_plus, passtime, Probability_plus, Flow_Prob_Beta, Fraction_A_state, Fraction_B_state, fraction_A_layer, fraction_B_layer


def repeated_and_mean():
    global MEAN_FLOW_PROB_BETA, PT, PB, PA, PAB, FA, FB, FAB, mean_Probability_plus, MEAN_Fraction_A_state, MEAN_Fraction_B_state
    PT = []  # 시간 측정값 리스트
    PB = []  # B_layer 노드의 평균값 리스트
    PA = []  # A_layer 노드의 평균값 리스트
    PAB = []
    FA = []
    FB = []
    FAB = []
    mean_Probability_plus = []  # +로 consensus 되는 확률 리스트
    MEAN_FLOW_Prob_Beta = pd.DataFrame()
    MEAN_FLOW_PROB_BETA = pd.DataFrame()
    MEAN_fraction_A_state = pd.DataFrame()
    MEAN_Fraction_A_state = pd.DataFrame()
    MEAN_fraction_B_state = pd.DataFrame()
    MEAN_Fraction_B_state = pd.DataFrame()
    for i in range(repeating_number):
        AL.select_layer_A_model()
        BL.select_layer_B_model()
        BL.making_interconnected_edges()
        interconnected_dynamics()
        PT.append(passtime)
        PB.append(B_plus / B_node)
        PA.append(A_plus / A_node)
        PAB.append((B_plus / B_node) + (A_plus / A_node))
        FA.append(fraction_A_layer)
        FB.append(fraction_B_layer)
        FAB.append(fraction_A_layer + fraction_B_layer)
        mean_Probability_plus.append(Probability_plus)
        MEAN_FLOW_Prob_Beta = pd.concat([MEAN_FLOW_Prob_Beta, Flow_Prob_Beta], axis=1,
                                        ignore_index=True)  # 반복횟수에 따라 칼럼병합
        MEAN_fraction_A_state = pd.concat([MEAN_fraction_A_state, Fraction_A_state], axis=1,
                                          ignore_index=True)  # 반복횟수에 따라 칼럼병합
        MEAN_fraction_B_state = pd.concat([MEAN_fraction_A_state, Fraction_B_state], axis=1,
                                          ignore_index=True)  # 반복횟수에 따라 칼럼병합

    MEAN_FLOW_PROB_BETA = MEAN_FLOW_Prob_Beta.fillna(0)  # 빈칸 0으로 채우기
    MEAN_Fraction_A_state = MEAN_fraction_A_state.fillna(0)
    MEAN_Fraction_B_state = MEAN_fraction_B_state.fillna(0)
    return PT, PB, PA, PAB, FA, FB, FAB, mean_Probability_plus, MEAN_FLOW_PROB_BETA, MEAN_Fraction_A_state, MEAN_Fraction_B_state







