import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys


def read_file(path):
    df = pd.read_csv(path)
    return df


v_sample = 0.4


def search_u(x, v, t, data):
    for i in range(len(data)):
        if (data[i][0] == x and
                data[i][1] == t):
            return data[i][v]
    return 0


def search_u1(x, v, y, data):
    for i in range(len(data)):
        if abs(data[i][0] - x) < 0.1 and abs(data[i][1] - y) < 0.1:
            return data[i][4]
    return 0


def search_u2(x, v, y, data):
    for i in range(len(data)):
        if abs(data[i][0] - x) < 0.1 and abs(data[i][1] - y) < 0.1:
            return data[i][5]
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


def draw_heat(data, path):
    real_data = np.array(data)
    x = generate_coordinate(real_data, 0)
    y = generate_coordinate(real_data, 1)
    x = np.array(x)
    y = np.array(y)

    x = np.arange(x.min(), x.max(), step=0.01)
    y = np.arange(y.min(), y.max(), step=0.01)

    X, Y = np.meshgrid(x, y)
    Z = []
    Q = []
    for i in range(len(X)):
        tmp = []
        for j in range(len(X[0])):
            u = search_u1(X[i][j], 4, Y[i][j], data)
            tmp.append(u)
        Z.append(tmp)
    Z = np.array(Z)

    for i in range(len(X)):
        tmp = []
        for j in range(len(X[0])):
            u = search_u2(X[i][j], 5, Y[i][j], data)
            tmp.append(u)
        Q.append(tmp)
    Q = np.array(Q)

    plt.streamplot(X, Y, Z, Q, density=[0.5, 1])
    plt.xlabel("x_coord")
    plt.ylabel("y_coord")
    plt.title("Field of Skin Friction Coefficient")
    save_path = path + "stream_ns.png"  # ----------------此处需修改------------------
    plt.savefig(save_path)


def select_v(data):
    real_data = []
    for i in range(len(data)):
        if data[i][1] == v_sample:
            real_data.append(data[i])
    return real_data


# ----------------------------------------------------------
#                   NS流场图
# 函数功能：读入NS方程.csv数据，画出流场图
# 参数(1个)：1.path: csv数据路径，str类型
# ----------------------------------------------------------
def execute(path, name):
    file_path = path + name
    data = pd.read_csv(file_path)
    df = data.drop('Global_Index', 1)
    data = df.values
    draw_heat(data, path)


def main():
    pyArgs = []
    pyArgs.append(sys.argv[1])
    pyArgs.append(sys.argv[2])
    execute(pyArgs[0], pyArgs[1])


if __name__ == '__main__':
    main()
