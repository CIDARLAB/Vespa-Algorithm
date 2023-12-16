import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import read_dot

# path = f"Section_1/Node1_10_7_3_5_2_1_2_0/Edge1|16_14_2_flow.dot"
# G = read_dot(path)
# pos = nx.spring_layout(G)
# color_list = ['blue' for i in range(len(G.nodes()))]
# nx.draw_networkx(G, pos, nodelist=G.nodes(), node_color=color_list)

import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件
for i in range(1, 4):
    df = pd.read_csv(f'comp_runtime{i}.csv')

    # 创建一个包含两个子图的画布
    fig, (comp_ax, upper_ax, middle_ax, lower_ax) = plt.subplots(4, 1, figsize=(16, 16), sharex=True)

    comp_ax.plot(df[df.columns[0]], df[df.columns[1]], label=df.columns[1], color='red')
    comp_ax.set_ylabel('Design Complexity')
    comp_ax.legend()
    comp_ax.grid(True)

    # Upper Subplot
    for col in df.columns[2:4]:
        upper_ax.plot(df[df.columns[0]], df[col], label=col)

    # 绘制基准线
    upper_ax.axhline(y=1, color='b', linestyle='--', label='Baseline (Runtime = 1s)')

    # remark as red if bigger than 60 and pass the validation.
    # remark as black if bigger than 60 but fail the validation.
    # mask = (df[df.columns[3]] > 60) & (df[df.columns[6]] == 1)
    # mask1 = (df[df.columns[3]] > 60) & (df[df.columns[6]] != 1)

    mask = (df[df.columns[3]] > 1)
    print(len(df[mask]))
    upper_ax.scatter(
        df[mask][df.columns[0]],  # x values
        df[mask][df.columns[3]],  # y values
        color='red'
    )
    # upper_ax.scatter(
    #     df[mask1][df.columns[0]],  # x values
    #     df[mask1][df.columns[3]],  # y values
    #     color='black'
    # )

    # label red points when their runtime is bigger than 60s
    upper_ax.set_ylabel('Runtime(s), All-type Constraint (#)')
    upper_ax.legend()
    upper_ax.grid(True)

    # Middle Subplot
    middle_ax.plot(df[df.columns[0]], df[df.columns[4]], label=df.columns[4], color="green")

    # 将与上面标红相对应的点也标红
    for x_val in df[mask][df.columns[0]]:
        corresponding_y_val = df[df[df.columns[0]] == x_val][df.columns[4]].values[0]
        middle_ax.scatter(x_val, corresponding_y_val, color='red')
    # for x_val in df[mask1][df.columns[0]]:
    #     corresponding_y_val = df[df[df.columns[0]] == x_val][df.columns[4]].values[0]
    #     middle_ax.scatter(x_val, corresponding_y_val, color='black')

    middle_ax.set_ylabel('NAND Constraints (#)')
    middle_ax.legend()
    middle_ax.grid(True)

    # Lower Subplot
    lower_ax.plot(df[df.columns[0]], df[df.columns[5]], label=df.columns[5], color="purple")

    # 将与上面标红相对应的点也标红
    for x_val in df[mask][df.columns[0]]:
        corresponding_y_val = df[df[df.columns[0]] == x_val][df.columns[5]].values[0]
        lower_ax.scatter(x_val, corresponding_y_val, color='red')
    # for x_val in df[mask1][df.columns[0]]:
    #     corresponding_y_val = df[df[df.columns[0]] == x_val][df.columns[5]].values[0]
    #     lower_ax.scatter(x_val, corresponding_y_val, color='black')

    # 添加图例
    lower_ax.set_xlabel('Benchmark ordered by complexity #')
    lower_ax.set_ylabel('# of Searched Graph')
    lower_ax.legend()
    lower_ax.grid(True)

    # save the figure
    plt.suptitle('Plot of Runtime and # of Searched Graph for Random Benchmark Section 3', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'Min_I_vs_Runtime{i}.png', dpi=300, bbox_inches='tight')





