import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


# 读取数据文件
def read_file(path, name):
    file_path = path + "/" + name
    df = pd.read_csv(file_path, header=None, sep='\t')
    return df


def relation_plot(df, path, c1, c2):
    col_1 = df[df.columns[c1]]
    col_2 = df[df.columns[c2]]
    _ = plt.plot(col_1, col_2)
    # save_path = "./src/main/resources/static/images/relation_plot"
    save_path = path + "relation_plot.png"
    # save_path = "D:/relation_plot.png"
    print("relation_plot path", save_path)
    plt.savefig(save_path)


if __name__ == '__main__':
    print("py main 1")
    pyArgs = []

    # for i in range(1, len(sys.argv)):
    pyArgs.append(sys.argv[1])
    pyArgs.append(sys.argv[2])
    pyArgs.append(int(sys.argv[3]))
    pyArgs.append(int(sys.argv[4]))

    print("py main 1")
    print("pyArgs[0]", pyArgs[0])
    print("pyArgs[1]", pyArgs[1])

    df = read_file(pyArgs[0], pyArgs[1])

    print("py main 2")

    relation_plot(df, pyArgs[0], pyArgs[2], pyArgs[3])

    print("py main 3")

    print(pyArgs[1] + pyArgs[2])
