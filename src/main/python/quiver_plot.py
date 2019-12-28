import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


# 读取数据文件
def read_file(path):
    df = pd.read_csv(path, header=None, sep='\t')
    return df


def quiver_plot(df, col1, col2):
    col1 = df[df.columns[col1]][:100]
    col2 = df[df.columns[col2]][:100]

    min_1 = np.floor(col1.min()) - 1
    max_1 = np.floor(col1.max())
    min_2 = np.floor(col2.min()) - 1
    max_2 = np.floor(col2.max())
    length = len(col1.index)

    X = np.arange(min_1, max_1, 0.02)
    Y = np.arange(min_2, max_2, 0.02)

    col1 = col1.values.reshape(length, 1)
    col2 = col2.values.reshape(length, 1)

    plt.quiver(X, Y, col1, col2, scale=0.4, width=0.005)
    save_path = "./src/main/resources/static/images/quiver_plot"
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
    quiver_plot(df, pyArgs[1], pyArgs[2])

    print(pyArgs[1] + pyArgs[2])
