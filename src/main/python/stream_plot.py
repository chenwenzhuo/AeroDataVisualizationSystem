import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


# 读取数据文件
def read_file(path):
    df = pd.read_csv(path, header=None, sep='\t')
    return df


def stream_plot(df, col1, col2):
    col1 = df[df.columns[col1]][:4228]
    col2 = df[df.columns[col2]][:4228]

    min_1 = np.floor(col1.min()) - 1
    max_1 = np.floor(col1.max())
    min_2 = np.floor(col2.min()) - 1
    max_2 = np.floor(col2.max())

    length = len(col1.index)
    lengthj = complex(len(col1.index))

    Y, X = np.mgrid[min_1:max_1:lengthj, min_2:max_2:lengthj]

    col1 = col1.values.reshape(length, 1)
    U_1 = np.tile(col1, length)

    col2 = col2.values.reshape(length, 1)
    V_1 = np.tile(col2, length)

    plt.streamplot(X, Y, U_1, V_1, density=[0.5, 1])
    save_path = "./src/main/resources/static/images/stream_plot"
    plt.savefig(save_path)
    # plt.show()


if __name__ == '__main__':
    pyArgs = []
    # for i in range(1, len(sys.argv)):
    #     pyArgs.append(int(sys.argv[i]))
    pyArgs.append(sys.argv[1])
    pyArgs.append(int(sys.argv[2]))
    pyArgs.append(int(sys.argv[3]))

    df = read_file(pyArgs[0])
    stream_plot(df, pyArgs[1], pyArgs[2])

    print(pyArgs[1] + pyArgs[2])
