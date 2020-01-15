import numpy as np
import matplotlib.pyplot as plt
import sys

v_sample = 0.4


def search_u(x, v, t, data):
    for i in range(len(data)):
        if (data[i][0] == x and
                data[i][1] == v and
                data[i][2] == t):
            return data[i][3]
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
    y = generate_coordinate(real_data, 2)

    X, Y = np.meshgrid(x, y)
    Z = []
    for i in range(len(X)):
        tmp = []
        for j in range(len(X[0])):
            u = search_u(X[i][j], v_sample, Y[i][j], data)
            tmp.append(u)
        Z.append(tmp)
    plt.contourf(X, Y, Z, 50, alpha=.75, cmap='jet')
    plt.xlabel("X")
    plt.ylabel("T")
    plt.title("Burgers Equation: Map of U")
    plt.colorbar()
    save_path = path + "heat_burg.png"  # ----------------此处需修改------------------
    plt.savefig(save_path)


def select_v(data):
    real_data = []
    for i in range(len(data)):
        if data[i][1] == v_sample:
            real_data.append(data[i])
    return real_data


# ----------------------------------------------------------
#                   Burgers热力图
# 函数功能：读入burgers方程的txt数据，画出热力图
# 参数(1个)：1.path: txt数据路径，str类型
# ----------------------------------------------------------
def execute(path, name):
    file_path = path + name
    data = np.loadtxt(file_path)
    data = select_v(data)
    draw_heat(data, path)


def main():
    pyArgs = []
    pyArgs.append(sys.argv[1])
    pyArgs.append(sys.argv[2])
    execute(pyArgs[0], pyArgs[1])


if __name__ == '__main__':
    main()
