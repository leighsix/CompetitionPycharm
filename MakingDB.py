import pandas as pd


class MakingDB:
    def __init__(self):



def making_dataframe():
    global data_result, DATA_MFPBS, DATA_MFAS, DATA_MFBS, ganma, beta, prob_p, prob_q, Ganma, Beta, mean_PB, mean_PA, mean_PT, mean_PAB, mean_P_plus, Prob_P, Prob_Q, mean_FA, mean_FB, mean_FAB

    mean_PT = []  # 시간측정 평균값 리스트
    mean_PB = []  # 반복횟수에 대한 B_layer 노드의 평균값
    mean_PA = []  # 반복횟수에 대한 A_layer 노드의 평균값
    mean_PAB = []
    mean_FA = []
    mean_FB = []
    mean_FAB = []
    mean_P_plus = []  # 반복횟수에 대한 +로 consensus 되는 확률의 평균값 리스트
    Ganma = []  # ganma 리스트
    Beta = []
    Prob_P = []  # 확률 P 리스트
    Prob_Q = []  # 확률 Q 리스트
    data_MFPBS = pd.DataFrame()
    Data_MFPBS = pd.DataFrame()
    DATA_MFPBS = pd.DataFrame()
    data_MFAS = pd.DataFrame()
    Data_MFAS = pd.DataFrame()
    DATA_MFAS = pd.DataFrame()
    data_MFBS = pd.DataFrame()
    Data_MFBS = pd.DataFrame()
    DATA_MFBS = pd.DataFrame()
    for ganma in r:
        for beta in D:
            MFPBS = []
            MFAS = []
            MFBS = []
            prob_p = ganma / (1 + ganma)  # 확률 p
            prob_q = 1 - prob_p  # 확률 q
            repeated_and_mean()
            Ganma.append(ganma)
            Beta.append(beta)
            Prob_P.append(prob_p)
            Prob_Q.append(prob_q)
            mean_PT.append(sum(PT) / repeating_number)
            mean_PB.append(sum(PB) / repeating_number)
            mean_PA.append(sum(PA) / repeating_number)
            mean_PAB.append(sum(PAB) / repeating_number)
            mean_FA.append(sum(FA) / repeating_number)
            mean_FB.append(sum(FB) / repeating_number)
            mean_FAB.append(sum(FAB) / repeating_number)
            mean_P_plus.append(sum(mean_Probability_plus) / repeating_number)
            MFPBS.append(ganma)
            MFPBS.append(beta)
            MFAS.append(ganma)
            MFAS.append(beta)
            MFBS.append(ganma)
            MFBS.append(beta)
            for i in range(len(MEAN_FLOW_PROB_BETA)):
                MFPB = np.mean(MEAN_FLOW_PROB_BETA.iloc[i])  # 반복횟수에 따른 베타확률의 평균값 정리
                MFPBS.append(MFPB)
            data_MFPBS = pd.DataFrame(MFPBS)  # 반복횟수별 평균값으로 칼럼으로 정리
            Data_MFPBS = pd.concat([Data_MFPBS, data_MFPBS], axis=1, ignore_index=True)  # 감마,베타별 변화상태 정리

            for i in range(len(MEAN_Fraction_A_state)):
                MFA = np.mean(MEAN_Fraction_A_state.iloc[i])  # 반복횟수에 따른 different state fraction의 평균값 정리
                MFAS.append(MFA)
            data_MFAS = pd.DataFrame(MFAS)  # 반복횟수별 평균값으로 칼럼으로 정리
            Data_MFAS = pd.concat([Data_MFAS, data_MFAS], axis=1, ignore_index=True)  # 감마,베타별 변화상태 정리

            for i in range(len(MEAN_Fraction_B_state)):
                MFB = np.mean(MEAN_Fraction_B_state.iloc[i])  # 반복횟수에 따른 different state fraction의 평균값 정리
                MFBS.append(MFB)
            data_MFBS = pd.DataFrame(MFBS)  # 반복횟수별 평균값으로 칼럼으로 정리
            Data_MFBS = pd.concat([Data_MFBS, data_MFBS], axis=1, ignore_index=True)  # 감마,베타별 변화상태 정리

            if beta % 1 == 0:
                print(ganma, beta, (sum(PT) / repeating_number), (sum(PB) / repeating_number),
                      (sum(PA) / repeating_number), (sum(PAB) / repeating_number))
    data_result = pd.DataFrame(
        {'ganma': Ganma, 'beta': Beta, 'A layer mean': mean_PA, 'B layer mean': mean_PB, 'A B layer mean': mean_PAB,
         'Probability + mean': mean_P_plus, 'Time mean': mean_PT, 'Prob_P': Prob_P,
         'Prob_Q': Prob_Q, 'Fraction A': mean_FA, 'Fraction B': mean_FB, 'Fraction AB': mean_FAB})
    DATA_MFPBS = Data_MFPBS.fillna(0)  # 빈칸은 0으로 채우기
    DATA_MFAS = Data_MFAS.fillna(0)  # 빈칸은 0으로 채우기
    DATA_MFBS = Data_MFBS.fillna(0)  # 빈칸은 0으로 채우기
    return data_result, DATA_MFPBS, DATA_MFAS, DATA_MFBS


def saving_data(a):
    Total_data.to_pickle('result' + str(a) + '_data.pickle')
    DATA_MFPBS.to_pickle('flow_prob_beta' + str(a) + '_data.pickle')
    DATA_MFAS.to_pickle('A_different_state' + str(a) + '_data.pickle')
    DATA_MFBS.to_pickle('B_different_state' + str(a) + '_data.pickle')


def pandas_concat1(a, b, c, d, e):  # pandas-concat('결과1', '결과2', '저장할 이름')
    result_1 = pd.read_pickle(a)
    result_2 = pd.read_pickle(b)
    result_3 = pd.read_pickle(c)
    result_4 = pd.read_pickle(d)
    final_result = pd.concat([result_1, result_2, result_3, result_4], ignore_index=True)
    final_result_dropped = final_result.drop_duplicates(['ganma', 'beta'], keep='first')
    final_result_dropped.to_pickle(e)


def pandas_concat2(a, b, c, d, e):  # pandas-concat('결과1', '결과2', '저장할 이름')
    result_1 = pd.read_pickle(a)
    result_2 = pd.read_pickle(b)
    result_3 = pd.read_pickle(c)
    result_4 = pd.read_pickle(d)
    final_result1 = pd.concat([result_1, result_2], axis=1, ignore_index=True)
    final_result2 = pd.concat([result_3, result_4], axis=1, ignore_index=True)
    final_result3 = pd.concat([final_result1, final_result2], axis=1, ignore_index=True)
    final_result3.to_pickle(e)

def different_state_ratio(filename, time, new_filename):  # different state ratio로 편집해주는 함수
    reading_file = pd.read_pickle(filename)
    index_g = (reading_file.iloc[0, :])  ## ganma index 지정
    index_b = reading_file.iloc[1, :]  ## beta index 지정
    index_t = []  ## time index 지정
    for i in range(0, time):
        index_t.append(i)
    different_state = reading_file.iloc[2:, :]
    dic = {}
    for i in range(len(index_g)):
        for j in range(0, time):
            data = different_state.iloc[j, i]
            dic[index_g[i], index_b[i], j] = data
    frame = pd.Series(dic)
    frame.index.names = ['ganma', 'beta', 'time']
    df = frame.reset_index(name='Fraction Different')
    DF = df.set_index(['ganma', 'beta', 'time'])
    final_table = DF.pivot_table('Fraction Different', 'time', ['beta', 'ganma'])
    final_table.to_pickle(new_filename)
    return final_table


def flow_prob_beta_dataframe(filename, time, new_filename):  # different state ratio로 편집해주는 함수
    reading_file = pd.read_pickle(filename)
    index_g = (reading_file.iloc[0, :])  ## ganma index 지정
    index_b = reading_file.iloc[1, :]  ## beta index 지정
    index_t = []  ## time index 지정
    for i in range(0, time):
        index_t.append(i)
    flow_prob_beta = reading_file.iloc[2:, :]
    dic = {}
    for i in range(len(index_g)):
        for j in range(0, time):
            data = flow_prob_beta.iloc[j, i]
            dic[index_g[i], index_b[i], j] = data
    frame = pd.Series(dic)
    frame.index.names = ['ganma', 'beta', 'time']
    df = frame.reset_index(name='Flow_prob_beta')
    DF = df.set_index(['ganma', 'beta', 'time'])
    final_table = DF.pivot_table('Flow_prob_beta', 'time', ['beta', 'ganma'])
    final_table.to_pickle(new_filename)
    return final_table