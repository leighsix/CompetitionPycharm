def plot_3D(result, a, b, c, d, e,
            f):  # ex__  plot_3D('result11_data2.pickle', 'ganma', 'beta', 'B layer mean', 45, 45, 'A b layer mean')
    sns.set_style("whitegrid")
    final_data = pd.read_pickle(result)
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(final_data[a], final_data[b], final_data[c], cmap='RdBu', edgecolor='none')
    ax.set_xlabel(str(a))
    ax.set_ylabel(str(b))
    ax.set_zlabel(str(c))
    ax.set_title(str(f))
    ax.view_init(d, e)
    # ax.scatter(final_data[a], final_data[b], final_data[c], c=final_data[c], cmap='RdBu', linewidth=0.1) ax.view_init(d, e)


def plot_2D(result, a, b, c, d,
            e):  # ex__  plot_2D('result2.3_data.pickle', 'beta', 'B layer mean', 'ganma', 1.0, 'ganma = 1')
    sns.set_style("whitegrid")
    final_data = pd.read_pickle(result)
    mini = final_data[final_data[c] > (d - 0.01)]
    two_dimension = mini[mini[c] < (d + 0.01)]
    plt.plot(two_dimension[a], two_dimension[b], '-', label=e)
    plt.legend(framealpha=1, frameon=True)
    plt.ylim(-1.1, 1.1)
    plt.xlabel(str(a))
    plt.ylabel(str(b))


def prob_beta_plot_3D(result, number_ganma, t, initial, gap, a, b, c, d, e):
    flow_probbeta_data = pd.read_pickle(result)
    ganma_data = []
    probbeta = []
    times = np.linspace(0, t - 1, t)
    time = sorted(sorted(times) * number_ganma)
    for i in range(number_ganma):
        ganma_data.append(flow_probbeta_data.iloc[0, initial + (gap * i)])
    ganma_datas = (ganma_data) * t
    for j in range(t):
        for i in range(number_ganma):
            probbeta.append(flow_probbeta_data.iloc[2 + j, initial + (gap * i)])
    sns.set_style("whitegrid")
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(time, ganma_datas, probbeta, cmap='viridis', edgecolor='none')
    ax.set_xlabel(str(a))
    ax.set_ylabel(str(b))
    ax.set_zlabel(str(c))
    ax.view_init(d, e)


# ex__  prob_beta_plot_3D('flow_prob_beta5.0_data.pickle', 51, 20, 10, 101, 'time', 'ganma', 'prob_beta', 45, 45)

def total_flow_prob_beta_chart(filename):
    plt.figure()
    sns.set()
    da = pd.read_pickle(filename)
    plt.plot(da, linewidth=0.2)
    plt.ylabel('probability for layer B')
    plt.xlabel('time(step)')


def total_different_state_ratio_chart(filename, ylabel):
    plt.figure()
    sns.set()
    da = pd.read_pickle(filename)
    plt.plot(da, linewidth=0.2)
    plt.ylabel(ylabel)
    plt.xlabel('time(step)')


def beta_scale_for_chart(filename, y_axis, a, b):  # 0 < a, b < 3
    plt.figure()
    sns.set()
    da = pd.read_pickle(filename)
    plt.ylim(-0.5, 0.5)
    plt.ylabel(y_axis)
    plt.xlabel('time(step)')
    beta_scale = da.columns.levels[0]
    min_beta = sum(beta_scale < a)
    max_beta = sum(beta_scale < b)
    for i in range(min_beta, max_beta):
        pic = da[beta_scale[i]]
        plt.plot(pic, linewidth=0.3)


def ganma_scale_for_chart(filename, y_axis, a, b):  # 0 < a, b < 3
    plt.figure()
    sns.set()
    da = pd.read_pickle(filename)
    unstack = da.unstack()
    reset = unstack.reset_index(name='different_state')
    Reset = pd.DataFrame(reset)
    final_table = Reset.pivot_table('different_state', 'time', ['ganma', 'beta'])
    plt.ylim(-0.5, 0.5)
    plt.ylabel(y_axis)
    plt.xlabel('time(step)')
    ganma_scale = final_table.columns.levels[0]
    min_beta = sum(ganma_scale < a)
    max_beta = sum(ganma_scale < b)
    for i in range(min_beta, max_beta):
        pic = final_table[ganma_scale[i]]
        plt.plot(pic, linewidth=0.3)


def z_function(result, a):
    final_data = pd.read_pickle(result)
    z = np.array(final_data[str(a)]).reshape(41, 41)
    Z = np.zeros((1681, 1681))
    for i in range(0, 41):
        for j in range(0, 41):
            for k in range(0, 41):
                for l in range(0, 41):
                    Z[(i * 41) + k][(j * 41) + l] = z[i][j]
    return Z

# plot_3D_to_2D_contour('result128128_1(5)_1(5)ver2_data.pickle', 'beta','ganma', 'A B layer mean','beta', 'ganma', 'A B layer mean')
def plot_3D_to_2D_contour(result, a, b, c, d, e, f):
    sns.set_style("whitegrid")
    final_data = pd.read_pickle(result)
    result_a = sorted(np.array(final_data[str(a)]))
    result_b = sorted(np.array(final_data[str(b)]))
    result_c = np.array(final_data[str(c)]).reshape(41, 41)
    X, Y = np.meshgrid(result_a, result_b)
    Z = z_function(result, c)
    plt.contourf(X, Y, Z, 50, cmap='RdBu')
    plt.xlabel(str(d))
    plt.ylabel(str(e))
    plt.colorbar(label=str(f))