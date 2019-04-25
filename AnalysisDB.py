import Setting_Simulation_Value
import sqlalchemy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sympy import *
import SelectDB
import seaborn as sns
from mpl_toolkits.mplot3d.axes3d import *
matplotlib.use("TkAgg")


class AnalysisDB:
    def __init__(self):
        self.select_db = SelectDB.SelectDB()

    def making_property_array_for_new(self, setting, step):
        property_array = np.zeros(5)
        df_original = self.select_db.select_data_from_DB(setting)
        df_step = df_original[df_original.Steps == step]
        model = df_step['MODEL']
        model = sorted(model.unique())
        for m in model:
            df_model = df_step[df_step.MODEL == m]
            total_AS = self.calculate_total_AS_new(df_model)
            pcr, ncr = self.calculate_consensus_number_new(df_model)
            initial_value = np.array([m, total_AS, pcr, ncr, pcr+ncr])
            property_array = np.vstack([property_array, initial_value])
        property_data = property_array[1:]
        columns = ['Model', 'AS total', 'PCR', 'NCR', 'CR']
        df = pd.DataFrame(property_data, columns=columns)
        return df

    def making_property_array(self, setting, step):
        property_array = np.zeros(11)
        df_original = self.select_db.select_data_from_DB(setting)
        df_step = df_original[df_original.Steps == step]
        model = df_step['MODEL']
        model = sorted(model.unique())
        for m in model:
            df_model = df_step[df_step.MODEL == m]
            A_nodes = df_model['A_node_number']
            A_nodes = sorted(A_nodes.unique())
            for an in A_nodes:
                df_an = df_model[df_model.A_node_number == an]
                B_nodes = df_an['B_node_number']
                B_nodes = sorted(B_nodes.unique())
                for bn in B_nodes:
                    df_bn = df_an[df_an.B_node_number == bn]
                    A_edges = df_bn['A_internal_edges']
                    A_edges = sorted(A_edges.unique())
                    for ae in A_edges:
                        df_ae = df_bn[df_bn.A_internal_edges == ae]
                        B_edges = df_ae['B_internal_edges']
                        B_edges = sorted(B_edges.unique())
                        for be in B_edges:
                            df_be = df_ae[df_ae.B_internal_edges == be]
                            total_AS = self.calculate_total_AS(setting, df_be)
                            total_fraction_ab = self.calculate_fraction_ab_total(df_be)
                            pcr, ncr = self.calculate_consensus_number_old2(setting, df_be)
                            initial_value = np.array([m, an, bn, ae, be, step,
                                                      total_AS, total_fraction_ab, pcr,
                                                      ncr, pcr+ncr])
                            property_array = np.vstack([property_array, initial_value])
        property_data = property_array[1:]
        columns = ['Model', 'A nodes', 'B nodes', 'A edges', 'B edges', 'steps', 'AS total', 'Fraction AB total', 'PCR',
                   'NCR', 'CR']
        df = pd.DataFrame(property_data, columns=columns)
        return df


    def calculate_total_AS_new(self, df):
        total_AS = sum(df['AS']) / len(df)
        return total_AS

    def calculate_consensus_number_new(self, df):
        pos_con = 0
        neg_con = 0
        signed_CI = df['AS']
        for i in range(len(df)):
            if signed_CI.iloc[i] > 0.95:
                pos_con += 1
            elif signed_CI.iloc[i] < -0.95:
                neg_con += 1
        return pos_con/len(df), neg_con/len(df)

    def calculate_total_AS(self, setting, df):
        AS = (df['LAYER_A_MEAN'] / setting.MAX + df['LAYER_B_MEAN']) / 2
        total_AS = sum(AS) / len(AS)
        return total_AS

    def calculate_consensus_number(self, setting, df):
        pos_con = 0
        neg_con = 0
        consensus = df['CONSENSUS']
        signed_CI = df['LAYER_A_MEAN'] / setting.MAX + df['LAYER_B_MEAN']
        for i in range(len(df)):
            if consensus.iloc[i] > 0.95 and signed_CI.iloc[i] > 1.7:
                pos_con += 1
            elif consensus.iloc[i] > 0.95 and signed_CI.iloc[i] < -1.7:
                neg_con += 1
        return pos_con/len(df), neg_con/len(df)

    def calculate_consensus_number_old(self, setting, df):  # 옛날 버전에 적용할 consensus 수 계산 인덱스
        pos_con = 0
        neg_con = 0
        consensus = df['FRACTION_AB']
        signed_CI = (df['LAYER_A_MEAN'] / setting.MAX) + df['LAYER_B_MEAN']
        for i in range(len(df)):
            if consensus.iloc[i] > 1.95 and signed_CI.iloc[i] > 1.9:
                pos_con += 1
            elif consensus.iloc[i] < 0.05 and signed_CI.iloc[i] < -1.9:
                neg_con += 1
        pos_con = pos_con / len(df)
        neg_con = neg_con / len(df)
        return pos_con, neg_con

    def calculate_consensus_number_old2(self, setting, df):  # 옛날 버전에 적용할 consensus 수 계산 인덱스
        pos_con = 0
        neg_con = 0
        signed_CI = (df['LAYER_A_MEAN'] / setting.MAX) + df['LAYER_B_MEAN']
        for i in range(len(df)):
            if signed_CI.iloc[i] > 1.95:      # 원래 1.9
                pos_con += 1
            elif signed_CI.iloc[i] < -1.95:   # 원래 -1.9
                neg_con += 1
        pos_con = pos_con / len(df)
        neg_con = neg_con / len(df)
        return pos_con, neg_con

    def calculate_fraction_ab_total(self, df):
        fraction_ab = df['FRACTION_A'] + df['FRACTION_B']
        total_fraction_ab = sum(fraction_ab) / len(fraction_ab)
        return total_fraction_ab

    def making_hist_for_pcr(self, df):
        fig = plt.figure()  # 그래프 창생성
        ax = fig.add_subplot(111)
        N = len(df)
        tuples = self.making_tuple_data(df)
        PCRs = tuples[1]  # 남학생 수
        NCRs = tuples[2]  # 여학생 수
        ind = np.arange(N)  # x축
        width = 0.3  # 너비
        p1 = ax.bar(ind, PCRs, width, color='SkyBlue')  # subplot에 bar chart 생성(남학생)
        p2 = ax.bar(ind, NCRs, width, color='IndianRed', bottom=PCRs)  # subplot에 bar chart 생성(여학생), bottom 옵션에 남학생 위에다 그리기
        ax.set_ylabel('ratio of state', fontsize=16)  # y축 라벨
        ax.set_xlabel('model', fontsize=16)  # x축 라벨
        ax.set_title('consensus ratio of models', fontsize=18)  # subplot의 제목
        ax.set_yticks(np.arange(0, 1.2, 0.2))  # 0 ~ 81까지 10간격식으로 y축 틱설정
        ax.set_xticks(ind)  # x축 틱설정
        ax.set_xticklabels(tuples[0])  # x축 틱 라벨설정
        ax.tick_params(labelsize=11)
        plt.legend((p1[0], p2[0]), ("PCR", "NCR"), loc=0, fontsize=14)
        plt.show()
        plt.close()

    def making_hist_for_index(self, df):
        N = len(df)
        tuples = self.making_tuple_data(df)
        CIs = tuples[4]
        FRs = tuples[5]
        CRs = tuples[6]
        ind = np.arange(N)  # x축
        width = 0.2  # 너비
        fig, ax = plt.subplots()

        p1 = ax.bar(ind - width, CIs, width, color='SkyBlue', label='AS')
        p2 = ax.bar(ind, FRs, width, color='IndianRed', label='FR')
        p3 = ax.bar(ind + width, CRs, width, color='green', label='CR')  # subplot에 bar chart 생성(여학생), bottom 옵션에 남학생 위에다 그리기
        ax.set_ylabel('values', fontsize=18)  # y축 라벨
        ax.set_xlabel('model', fontsize=18)  # x축 라벨
        ax.set_title('consensus index of models',  fontsize=18)  # subplot의 제목
        ax.set_yticks(np.arange(0, 2.2, 0.2))  # 0 ~ 81까지 10간격식으로 y축 틱설정
        ax.set_xticks(ind)  # x축 틱설정
        ax.set_xticklabels(tuples[0])  # x축 틱 라벨설정
        ax.tick_params(labelsize=8)
        plt.legend((p1[0], p2[0], p3[0]), ("CI", "FR", "CR"), loc=0, fontsize=14)
        plt.show()
        plt.close()

    def making_mixed_hist_new(self, df):
        fig = plt.figure()  # 그래프 창생성
        ax = fig.add_subplot(111)
        N = len(df)
        tuples = self.making_tuple_data_new(df)
        CIs = tuples[1]
        PCRs = tuples[2]  # 남학생 수
        NCRs = tuples[3]  # 여학생 수
        ind = np.arange(N)  # x축
        width = 0.2  # 너비
        p1 = ax.bar(ind-(width/2), PCRs, width, color='SkyBlue')  # subplot에 bar chart 생성(남학생)
        p2 = ax.bar(ind-(width/2), NCRs, width, color='IndianRed', bottom=PCRs)  # subplot에 bar chart 생성(여학생), bottom 옵션에 남학생 위에다 그리기
        p3 = ax.bar(ind+(width/2), CIs, width, color='palegreen', label='AS')

        ax.set_xlabel('model', fontsize=16)  # x축 라벨
        ax.set_title('Competition results', fontsize=18)  # subplot의 제목
        ax.set_yticks(np.arange(0, 1.2, 0.2))  # 0 ~ 81까지 10간격식으로 y축 틱설정
        ax.set_xticks(ind)  # x축 틱설정
        ax.set_xticklabels(tuples[0])  # x축 틱 라벨설정
        ax.tick_params(labelsize=13)
        plt.legend((p1[0], p2[0], p3[0]), ("PCR", "NCR", "AS total"), loc=0, fontsize=14)
        plt.show()
        plt.close()

    def making_mixed_hist(self, df):
        fig = plt.figure()  # 그래프 창생성
        ax = fig.add_subplot(111)
        N = len(df)
        tuples = self.making_tuple_data(df)
        PCRs = tuples[1]  # 남학생 수
        NCRs = tuples[2]  # 여학생 수
        CIs = tuples[3]
        ind = np.arange(N)  # x축
        width = 0.2  # 너비
        p1 = ax.bar(ind-(width/2), PCRs, width, color='SkyBlue')  # subplot에 bar chart 생성(남학생)
        p2 = ax.bar(ind-(width/2), NCRs, width, color='IndianRed', bottom=PCRs)  # subplot에 bar chart 생성(여학생), bottom 옵션에 남학생 위에다 그리기
        p3 = ax.bar(ind+(width/2), CIs, width, color='palegreen', label='AS')

        ax.set_xlabel('model', fontsize=16)  # x축 라벨
        ax.set_title('Competition results', fontsize=18)  # subplot의 제목
        ax.set_yticks(np.arange(0, 1.2, 0.2))  # 0 ~ 81까지 10간격식으로 y축 틱설정
        ax.set_xticks(ind)  # x축 틱설정
        ax.set_xticklabels(tuples[0])  # x축 틱 라벨설정
        ax.tick_params(labelsize=13)
        plt.legend((p1[0], p2[0], p3[0]), ("PCR", "NCR", "AS total"), loc=0, fontsize=14)
        plt.show()
        plt.close()

    def making_tuple_data_new(self, df):
        model = []
        As = []
        pcrs = []
        ncrs = []
        cr = []
        for i in df['Model']:
            model.append(i)
        model = tuple(model)
        for i in df['AS total']:
            As.append(eval(i))
        As = tuple(As)
        for i in df['PCR']:
            pcrs.append(eval(i))
        pcrs = tuple(pcrs)
        for i in df['NCR']:
            ncrs.append(eval(i))
        ncrs = tuple(ncrs)

        for i in df['CR']:
            cr.append(eval(i))
        cr = tuple(cr)
        return model, As, pcrs, ncrs, cr

    def making_tuple_data(self, df):
        model = []
        pcrs = []
        ncrs = []
        As = []
        fr = []
        cr = []
        for i in df['Model']:
            model.append(i)
        model = tuple(model)
        for i in df['PCR']:
            pcrs.append(eval(i))
        pcrs = tuple(pcrs)
        for i in df['NCR']:
            ncrs.append(eval(i))
        ncrs = tuple(ncrs)
        for i in df['AS total']:
            As.append(eval(i))
        As = tuple(As)
        for i in df['Fraction AB total']:
            fr.append(eval(i))
        fr = tuple(fr)
        for i in df['CR']:
            cr.append(eval(i))
        cr = tuple(cr)
        return model, pcrs, ncrs, As, fr, cr

 #'CI total', 'Fraction AB total', 'CR'
if __name__ == "__main__":
    print("AnalysisDB")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    analysis_db = AnalysisDB()
    setting.database = 'paper_revised_data'
    setting.table = 'simulation_table2'
    df = analysis_db.making_property_array_for_new(setting, 100)
    analysis_db.making_mixed_hist_new(df)

    


    # setting.database = 'competition'
    # setting.table = 'result_db'
    # df1 = analysis_db.making_property_array(setting, 30)
    # df2 = analysis_db.making_property_array(setting, 100)
    # setting.database = 'paper_revised_data'
    # setting.table = 'simulation_table'
    # df3 = analysis_db.making_property_array(setting, 100)
    # df = pd.concat([df1, df2, df3], ignore_index=True)
    # df = df.iloc[:, [0, 6, 8, 9, 10]]
    # print(df)
    # pd.to_pickle(df, 'df1')


    # fig.6
    # df = pd.concat([df1, df2], ignore_index=True)
    # df = df.loc[[9, 8, 1, 0, 3], :]
    # df['Model'] = ['RR(5)-RR(5)', 'RR(5)-BA', 'BA-RR(5)', 'BA-BA', 'RR(10)-RR(5)']
    # analysis_db.making_mixed_hist(df)

    # fig.5
    # df = pd.concat([df1, df2], ignore_index=True)
    # df = df.loc[[4, 5, 6, 9], :]
    # analysis_db.making_mixed_hist(df)

    # fig.4
    # setting.database = 'paper_revised_data'
    # setting.table = 'simulation_table'
    # df3 = analysis_db.making_property_array(setting, 100)

    # df = analysis_db.making_property_array_for_new(setting, 100)
    # analysis_db.making_mixed_hist_new(df)


    # df = pd.concat([df2, df3], ignore_index=True)
    # df = df.loc[[0, 2, 4, 6, 1, 3, 5], :]
    # df['Model'] = ['RRM', 'HM(2)', 'HM(4)', 'HM(8)', 'HM(16)', 'HM(32)', 'HM(64)']
    # analysis_db.making_mixed_hist(df)

    # df = df.iloc[:, [0, 6, 8, 9, 10]]
    # print(df)
    # for i in [0, 2, 4, 6, 1, 3, 5]:
    #     print(df.iloc[i, :])
    # analysis_db.making_mixed_hist(df)

    #
    # df.iloc[0, 0] = 'LM(1)'




    #analysis_db.making_hist_for_pcr(df)
    # analysis_db.making_mixed_hist(df)

    # df = df.loc[[7, 9, 8, 1, 0, 3, 4, 5, 6, 11, 13, 15, 10, 12, 14], :]
    # df = df.loc[[4, 5, 6, 7], :]
    # df = df.loc[[7, 8, 1, 0, 3], :]

    # df.iloc[0, 0] = 'BM(30)'
    # df.iloc[1, 0] = 'BM(100)'


    # df = df.iloc[:, [0, 6, 8, 9, 10]]
    # for i in range(15):
    #     print(df.iloc[i, :])


    # print(df)

    # for i in range(len(df)):
    #     print(df['Model'][i], df['AS total'][i])
    #print(df['Model'])
    #df = df.iloc[4:8, :]
    #df = df.loc[[7, 1, 3, 0, 8], :]

    #'CI total', 'Fraction AB total', 'PCR', 'NCR', 'CR'
    #df = df[df.Model == 'LM']
    #print(df['AS total'])


    #print(format(eval(df['CR']), '10.4f'), format(eval(df['NCR']), '10.4f'), format(eval(df['PCR']), '10.4f'))
    # df = df.sort_values(by='CR', ascending=False)
    # print(tuple(df['Model']))
    #
    # df = df.sort_values(by='NCR', ascending=False)
    # print(tuple(df['Model']))
    #
    # df = df.sort_values(by='PCR', ascending=False)
    # print(tuple(df['Model']))



    #tuples = analysis_db.making_tuple_data(df)
    #

    # NCRs = tuple(array['NCR'])
    # Coexs = tuple(array['CR'])
    # print(Coexs)











