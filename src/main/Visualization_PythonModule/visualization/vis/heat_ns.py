import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys


def read_file(path):
    df = pd.read_csv(path)
    return df


v_sample = 0.4


def search_u2(x, title_col, t, data):
    for i in range(len(data)):
        if (data[i][0] == x and
                data[i][1] == t):
            return data[i][title_col]
    return 0


def search_u(x, title_col, y, data):
    for i in range(len(data)):
        if abs(data[i][0] - x) < 0.002 and abs(data[i][1] - y) < 0.002:
            return data[i][title_col]
    return 0


def generate_coordinate(data, col):
    X = []
    for i in range(len(data)):
        tmp = data[i][col]
        exist = False
        for j in range(len(X)):
            if tmp == X[j]:
                exist = True
                break
        if not exist:
            X.append(tmp)
    return X


def draw_heat(data, title_col, title, path):
    real_data = np.array(data)
    x = generate_coordinate(real_data, 0)
    y = generate_coordinate(real_data, 1)

    X, Y = np.meshgrid(x, y)
    Z = []
    for i in range(len(X)):
        tmp = []
        for j in range(len(X[0])):
            u = search_u(X[i][j], title_col, Y[i][j], data)
            tmp.append(u)
        Z.append(tmp)

    plt.contourf(X, Y, Z, 8, alpha=.75, cmap='jet')
    plt.xlim(0, 1)
    plt.ylim(-0.5, 0.5)
    plt.xlabel("x_coord")
    plt.ylabel("y_coord")
    plt.title("NS Equation: %s" % title)
    plt.colorbar()

    ax = plt.gca()  # 获取当前坐标的位置
    ax.spines['right'].set_color('None')
    ax.spines['top'].set_color('None')
    # 指定坐标的位置
    ax.xaxis.set_ticks_position('bottom')  # 设置bottom为x轴
    ax.yaxis.set_ticks_position('left')  # 设置left为x轴
    ax.spines['bottom'].set_position(('data', 0))  # 这个位置的括号要注意
    ax.spines['left'].set_position(('data', 0))
    save_path = path + "heat_ns.png"  # ----------------此处需修改------------------
    plt.savefig(save_path)


def select_v(data):
    real_data = []
    for i in range(len(data)):
        if data[i][1] == v_sample:
            real_data.append(data[i])
    return real_data


# ----------------------------------------------------------
#                   NS热力图
# 函数功能：读入ns方程的csv数据，画出热力图
# 参数(2个)：1.path: csv数据路径，str类型
#           2.title_col: 热力图第三个维度的列，int类型
# ----------------------------------------------------------
def execute(path, name, title_col):
    file_path = path + name
    data = pd.read_csv(file_path)
    df = data.drop('Global_Index', 1)
    title = df.columns[title_col]
    data = df.values
    draw_heat(data, title_col, title, path)


def main():
    pyArgs = []
    pyArgs.append(sys.argv[1])
    pyArgs.append(sys.argv[2])
    pyArgs.append(int(sys.argv[3]))

    execute(pyArgs[0], pyArgs[1], pyArgs[2])


if __name__ == '__main__':
    main()
